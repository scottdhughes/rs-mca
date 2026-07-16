#!/usr/bin/env python3
"""Exact arithmetic audit for the conditional retained-lift appendix in v8.

The calculations below assume the paper's Parameter-retained factor lift.
They verify RF1--RF7 numerically, but they do NOT prove or discharge that
factor-lifting assumption and therefore create no unconditional MCA result.
"""

from fractions import Fraction
from math import log2


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def check_rows() -> None:
    p = (1 << 31) - (1 << 24) + 1
    q = p**6
    n = 1 << 21
    tiny = Fraction(1, 1 << 64)
    budget = q // (1 << 128)
    require(p == 127 * (1 << 24) + 1, "KoalaBear Proth decomposition is wrong")
    require(127 < (1 << 24) and 127 % 2 == 1, "invalid Proth coefficient")
    require(pow(3, (p - 1) // 2, p) == p - 1,
            "KoalaBear Proth certificate failed")
    require((p - 1) % n == 0, "KoalaBear subgroup divisibility failed")
    require(budget == 274980728111395087, "printed KoalaBear budget is wrong")

    rows = (
        # rate denominator, r, m, U, V, W, RF4 margin, RF2 top margin,
        # U-K(V-1), RF5 ceiling, printed safe bits, printed tangent gap
        (2, 611982, 119, 176735230, 169, 27525,
         4889934, 152123705899212, 574462,
         274589064742726105, 128.002056, 38.706920),
        (4, 1045433, 104, 109378776, 209, 29028,
         13182624, 113730027157979, 326872,
         274721012201264929, 128.001363, 37.935074),
        (8, 1352390, 90, 67028580, 256, 31500,
         11133440, 63736189920080, 181860,
         274578888391530706, 128.002110, 37.562917),
        (16, 1569744, 78, 41137824, 314, 34101,
         4204064, 32093320774290, 112288,
         274861787390229386, 128.000624, 37.349385),
    )

    for denominator, r, m, u_count, v_count, w_count, rf4_margin, top_margin, rank_margin, expected_bound, expected_bits, expected_gap in rows:
        k = n // denominator
        agreement = n - r
        dx = Fraction(u_count - 1) + tiny
        dy = Fraction(v_count - 1) + tiny
        dz = Fraction(w_count - 1) + tiny

        # RF1 and the exact convention/rounding identities.
        require(u_count == m * agreement, "U=mA identity failed")
        require(v_count >= m and w_count >= v_count, "RF1 size ordering failed")
        require(u_count - k * (v_count - 1) == rank_margin,
                "printed U-K(V-1) margin is wrong")
        require(rank_margin > 0, "RF1 rank margin is not positive")
        require(dx < m * agreement, "RF1 D_X<mA failed")
        require(Fraction(m * agreement) - dx == 1 - tiny,
                "printed D_X margin is wrong")
        require(p > v_count - 1, "RF1 characteristic bound failed")

        # RF2: integer top-degree comparison and field-size comparison.
        actual_top_margin = ((agreement - k - 1) * (2 * u_count - 1)
                             - (n - k - 1) * (2 * k + 1))
        require(actual_top_margin == top_margin,
                "printed RF2 top-degree margin is wrong")
        require(top_margin > 0, "RF2 top-degree comparison failed")
        require(Fraction(q) > 2 * u_count * dy,
                "RF2 field-size comparison failed")

        # RF4: exact coefficient count minus exact multiplicity conditions.
        coefficients = sum((u_count - k * j) * (w_count - j)
                           for j in range(v_count))
        conditions = n * sum((w_count - s) * (m - s)
                             for s in range(m))
        require(coefficients - conditions == rf4_margin,
                "printed RF4 interpolation margin is wrong")
        require(rf4_margin > 0, "RF4 strict interpolation count failed")

        # RF5--RF7: exact retained numerator and its two printed log columns.
        threshold = (2 * u_count * dy * dy * dz + (r + 1) * dy)
        retained = ceil_fraction(threshold)
        require(retained == expected_bound, "printed RF5 numerator is wrong")
        require(retained <= budget, "conditional retained numerator exceeds budget")
        safe_bits = log2(q) - log2(retained)
        tangent_gap = log2(retained) - log2(r + 1)
        require(abs(safe_bits - expected_bits) < 0.5e-6,
                "printed RF7 security bits do not round correctly")
        require(abs(tangent_gap - expected_gap) < 0.5e-6,
                "printed RF7 tangent gap does not round correctly")


def main() -> None:
    check_rows()
    print("v8 conditional retained-lift arithmetic: all checks passed")
    print("NOTE: the Parameter-retained factor lift remains an assumption.")


if __name__ == "__main__":
    main()
