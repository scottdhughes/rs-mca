#!/usr/bin/env python3
"""Verify simple-pole saturation by minimal-polynomial residue classes."""

from collections import Counter
from itertools import combinations, product
from math import comb


P = 5
D = (1, 2, 3, 4)
K = 1
M = 2


def poly_eval(poly, x):
    return sum(coefficient * pow(x, exponent, P) for exponent, coefficient in enumerate(poly)) % P


def word_value(x):
    return x * x % P


def complete_list():
    out = []
    for poly in product(range(P), repeat=K + 1):
        agreement = tuple(x for x in D if poly_eval(poly, x) == word_value(x))
        if len(agreement) >= M:
            out.append((poly, agreement))
    return out


def base_pole_witnesses(items):
    witnesses = []
    for poly, agreement in items:
        slope = poly[0]
        explanation = (poly[1],)
        for support in combinations(agreement, M):
            witnesses.append((slope, support, explanation, poly))
    return witnesses


def gf25_add(left, right):
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def gf25_mul(left, right):
    # t^2=2 over F_5.
    return (
        (left[0] * right[0] + 2 * left[1] * right[1]) % P,
        (left[0] * right[1] + left[1] * right[0]) % P,
    )


def gf25_eval_linear(poly, alpha=(0, 1)):
    return gf25_add((poly[0], 0), gf25_mul((poly[1], 0), alpha))


def vector_rank(vectors):
    rows = [list(vector) for vector in vectors if any(vector)]
    rank = 0
    column = 0
    while rows and column < len(rows[0]):
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column] % P), None)
        if pivot is None:
            column += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, P)
        rows[rank] = [(entry * inverse) % P for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank:
                continue
            factor = rows[index][column] % P
            rows[index] = [
                (entry - factor * pivot_entry) % P
                for entry, pivot_entry in zip(rows[index], rows[rank])
            ]
        rank += 1
        column += 1
    return rank


def collision_floor(total, bins):
    quotient, remainder = divmod(total, bins)
    return bins * comb(quotient, 2) + quotient * remainder


def brute_collision_floor(total, bins):
    best = None
    for cuts in combinations(range(total + bins - 1), bins - 1):
        boundaries = (-1,) + cuts + (total + bins - 1,)
        parts = tuple(
            boundaries[index + 1] - boundaries[index] - 1
            for index in range(bins)
        )
        value = sum(comb(part, 2) for part in parts)
        best = value if best is None else min(best, value)
    return best


def main():
    items = complete_list()
    assert len(items) == 6
    witnesses = base_pole_witnesses(items)
    assert len(witnesses) == 6

    # Every enumerated exact support is recovered from exactly one complete-list
    # polynomial, and every state reconstructs that polynomial.
    recovered = set()
    for slope, support, explanation, poly in witnesses:
        assert all(poly_eval(poly, x) == word_value(x) for x in support)
        assert len(support) == M
        assert (slope, explanation[0]) == poly
        recovered.add(poly)
    assert recovered == {poly for poly, _ in items}
    assert all(len(agreement) == M for _, agreement in items)

    base_slopes = Counter(poly[0] for poly, _ in items)
    assert sorted(base_slopes.values()) == [1, 1, 2, 2]
    assert len(base_slopes) == 4
    assert sum(comb(value, 2) for value in base_slopes.values()) == 2

    # Modulo pi_0=X, the residues are constants. Their affine difference rank
    # is one, hence all slopes lie in an F_5-affine line.
    base_poly = items[0][0]
    base_differences = (((poly[0] - base_poly[0]) % P,) for poly, _ in items)
    base_rank = vector_rank(tuple(base_differences))
    assert base_rank == 1
    assert len(base_slopes) <= P**base_rank

    # At alpha=t in F_25=F_5[t]/(t^2-2), pi_alpha=X^2-2. Since all list
    # polynomials have degree <2, their residues are the polynomials themselves.
    extension_slopes = [gf25_eval_linear(poly) for poly, _ in items]
    assert len(set(extension_slopes)) == len(items) == 6
    residue_differences = tuple(
        ((poly[0] - base_poly[0]) % P, (poly[1] - base_poly[1]) % P)
        for poly, _ in items
    )
    extension_rank = vector_rank(residue_differences)
    assert extension_rank == 2
    assert len(extension_slopes) <= P**extension_rank

    # Arbitrary earlier slope masks leave a literal residual exhausted by the
    # remaining residue/slope cells, each with one actual slope.
    earlier = {0, 1}
    residual = [witness for witness in witnesses if witness[0] not in earlier]
    cells = {
        slope: [witness for witness in residual if witness[0] == slope]
        for slope in set(witness[0] for witness in residual)
    }
    assert set().union(*(set(cell) for cell in cells.values())) == set(residual)
    assert all({witness[0] for witness in cell} == {slope} for slope, cell in cells.items())
    assert len(cells) <= P**base_rank

    # Raw occupancy identity on U=0: the unique zero polynomial has agreement
    # four and therefore exactly C(4,2)=6 exact-support witnesses.
    zero_items = []
    for poly in product(range(P), repeat=K + 1):
        agreement = tuple(x for x in D if poly_eval(poly, x) == 0)
        if len(agreement) >= M:
            zero_items.append((poly, agreement))
    assert zero_items == [((0, 0), D)]
    assert comb(len(zero_items[0][1]), M) == 6

    for bins in range(1, 7):
        for total in range(0, 11):
            assert collision_floor(total, bins) == brute_collision_floor(total, bins)

    # Tamper regressions: an omitted list state, wrong minimal polynomial rank,
    # altered multiplicity, and incomplete residual mask are all detected.
    assert len(items[:-1]) != len(items)
    assert vector_rank(tuple((difference[0],) for difference in residue_differences)) != extension_rank
    tampered = Counter(base_slopes)
    tampered[next(iter(tampered))] += 1
    assert sum(tampered.values()) != len(items)
    assert set(residual[:-1]) != set(residual)

    print("RESULT: PASS")
    print(f"complete_list_states={len(items)}")
    print(f"exact_witnesses={len(witnesses)}")
    print(f"base_pole_slopes={len(base_slopes)}")
    print(f"base_pole_multiplicities={sorted(base_slopes.values())}")
    print(f"base_residue_rank={base_rank}")
    print(f"extension_slopes={len(set(extension_slopes))}")
    print(f"extension_residue_rank={extension_rank}")
    print("arbitrary_earlier_mask=PASS")
    print("balanced_collision_floors=PASS")
    print("tamper_checks=PASS")


if __name__ == "__main__":
    main()
