#!/usr/bin/env python3
"""Exact arithmetic checks for the unconditional finite rows in v8.

This script verifies the printed Proth certificates, field budgets,
quadratic-boundary signs, paving-envelope divisions, all-radius saturation
inequalities, and circle-row arithmetic.  It uses only Python's standard
library and does not attempt to verify any conditional appendix statement.
"""

from math import comb, log2


TWO128 = 1 << 128


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def proth_certificate(p: int, u: int, s: int, witness: int) -> None:
    require(p == u * (1 << s) + 1, "incorrect Proth decomposition")
    require(u & 1 == 1, "Proth coefficient is not odd")
    require(u < (1 << s), "Proth coefficient is too large")
    require(pow(witness, (p - 1) // 2, p) == p - 1,
            "Proth modular certificate failed")


def paving_numerator(n: int, k: int, a: int) -> int:
    """The challenge-free integrated MDS paving envelope."""
    return min(comb(n, a), comb(n, k + 1) // comb(a - 1, k))


def beyond_johnson(n: int, k: int, a: int) -> bool:
    """Exact form of (n-a)/n > 1-sqrt(k/n)."""
    return k * n > a * a


def lucas_lehmer(exponent: int) -> bool:
    """Lucas--Lehmer test for the Mersenne number 2^exponent-1."""
    mersenne = (1 << exponent) - 1
    value = 4
    for _ in range(exponent - 2):
        value = (value * value - 2) % mersenne
    return value == 0


def check_prize_proth_rows() -> None:
    k = 1 << 40
    rows = (
        # rate denominator, n exponent, B, p, s, u, witness, bit length,
        # F(B-1), F(B), printed remainder
        (2, 41, 389500552609,
         132540169958804033333249306710494641010898987122689,
         92, 26766274163673319604503, 3, 167,
         5154112775168, -663955886271,
         1381541083842484386787422633985),
        (4, 42, 1210584858040,
         411940680852499481698306614369841346700408394874881,
         93, 41595378994516821279015, 13, 169,
         7590647904465, -3182321912768,
         2921538492713497448761933168641),
        (8, 43, 2879806199253,
         979947269755402568812854322316630667196565607677953,
         95, 24737346889219389259839, 5, 170,
         13908181940112, -6720484728007,
         2495687119199326634196634435585),
        (16, 44, 6233898019554,
         2121285573237585848299875619011192262679065433997313,
         97, 13387194060291799253121, 5, 171,
         19335616403905, -20973145690236,
         20440865928680199099134339186689),
    )

    for denominator, n_exponent, budget, p, s, u, witness, bits, f_left, f_right, remainder in rows:
        n = 1 << n_exponent
        require(n // k == denominator, "printed rate is inconsistent")
        proth_certificate(p, u, s, witness)
        require(p.bit_length() == bits, "printed field bit length is wrong")
        require(p < (1 << 256), "Prize field exceeds the printed ceiling")
        require((p - 1) % n == 0, "evaluation subgroup order does not divide p-1")
        quotient, actual_remainder = divmod(p, TWO128)
        require(quotient == budget, "printed 128-bit slope budget is wrong")
        require(actual_remainder == remainder, "printed budget remainder is wrong")
        require(0 < actual_remainder < TWO128, "budget remainder is out of range")

        redundancy = n - k

        def boundary(r: int) -> int:
            return r * r - n * (3 * r - redundancy)

        require(boundary(budget - 1) == f_left, "left boundary sign/value is wrong")
        require(boundary(budget) == f_right, "right boundary sign/value is wrong")
        require(f_left >= 0 > f_right, "quadratic boundary is not bracketed")


def check_special_saturation_and_paving_rows() -> None:
    p = (TWO128 - 255) * TWO128 + 1
    budget = TWO128 - 255
    proth_certificate(p, budget, 128, 3)
    require(p.bit_length() == 256 and p < (1 << 256),
            "special field is not a sub-2^256, 256-bit field")
    require(p // TWO128 == budget and p % TWO128 == 1,
            "special-field target budget is wrong")
    require((p - 1) % 512 == 0, "order-512 subgroup is unavailable")

    saturation_values = {
        64: 23582666872052266206656578733667004800,
        32: 4299074680733907393985381161600,
        16: 614965786737727286400,
        8: 19062702032000,
    }
    for k, printed in saturation_values.items():
        value = comb(128, k + 1)
        require(value == printed, "printed n=128 binomial value is wrong")
        require(value <= budget, "all-radius saturation budget fails")

    finite_rows = (
        (32, 52, 210954686508560867421211382134708972291),
        (64, 158, 275511258760747555342982982548156580976),
    )
    for k, a, printed in finite_rows:
        value = paving_numerator(512, k, a)
        require(value == printed, "printed finite paving numerator is wrong")
        require(value <= budget, "finite paving numerator exceeds the budget")
        require(beyond_johnson(512, k, a), "finite paving row is not beyond Johnson")


def check_circle_rows() -> None:
    exponent = 127
    p0 = (1 << exponent) - 1
    require(lucas_lehmer(exponent), "Lucas--Lehmer certificate failed")
    require((p0 + 1) % 512 == 0, "circle torus has no order-512 subgroup")
    q = p0 * p0
    budget = q // TWO128
    require(budget == 85070591730234615865843651857942052863,
            "printed circle budget is wrong")

    rows = (
        (32, 53, 81136417887908025931235146974888066266, 128.068311),
        (31, 50, 60827291905480389917403158602781524185, 128.483942),
    )
    for k, a, printed, printed_bits in rows:
        value = paving_numerator(512, k, a)
        require(value == printed, "printed circle paving numerator is wrong")
        require(value <= budget, "circle paving numerator exceeds the budget")
        require(beyond_johnson(512, k, a), "circle row is not beyond Johnson")
        bits = log2(q) - log2(value)
        require(abs(bits - printed_bits) < 0.5e-6,
                "printed circle security bits do not round correctly")


def main() -> None:
    check_prize_proth_rows()
    check_special_saturation_and_paving_rows()
    check_circle_rows()
    print("v8 unconditional arithmetic: all checks passed")


if __name__ == "__main__":
    main()
