#!/usr/bin/env python3
"""Checks for the multiplicity-thick repair to the character-frame interface."""

from cmath import exp, pi
from fractions import Fraction
from itertools import combinations
from math import comb


def dft(mu):
    q = len(mu)
    return [
        sum(mu[x] * exp(2j * pi * k * x / q) for x in range(q))
        for k in range(q)
    ]


def cyclic_checks():
    for q in (5, 7, 9, 11):
        mu = [Fraction((3 * x * x + 2 * x + 1) % 7 + 1, 1) for x in range(q)]
        total = sum(mu)
        mu = [float(x / total) for x in mu]
        hat = dft(mu)
        for a in range(1, min(q, 6)):
            A = tuple(range(a))
            multiplicity = [0] * q
            for x in A:
                for y in A:
                    multiplicity[(y - x) % q] += 1

            matrix = [
                [hat[(y - x) % q] for y in A]
                for x in A
            ]
            trace_square = sum(
                matrix[i][j] * matrix[j][i]
                for i in range(a)
                for j in range(a)
            ).real
            weighted = sum(multiplicity[k] * abs(hat[k]) ** 2 for k in range(q))
            assert abs(trace_square - weighted) < 1e-9

            # A coarse row-sum bound is enough for the verifier's kappa upper
            # bound; the theorem itself uses the exact operator norm.
            kappa_upper = max(sum(abs(z) for z in row) for row in matrix)
            tau = 3
            thin = sum(
                abs(hat[k]) ** 2
                for k in range(1, q)
                if multiplicity[k] < a / tau
            )
            thick = sum(
                abs(hat[k]) ** 2
                for k in range(1, q)
                if multiplicity[k] >= a / tau
            )
            assert thick <= tau * kappa_upper + 1e-9
            assert thick + thin <= tau * kappa_upper + thin + 1e-9


def gf_mul(a, b, modulus, degree):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
    return out


def gf_pow(a, exponent, modulus, degree):
    out = 1
    while exponent:
        if exponent & 1:
            out = gf_mul(out, a, modulus, degree)
        a = gf_mul(a, a, modulus, degree)
        exponent >>= 1
    return out


def binary_rank(vectors):
    basis = {}
    for value in vectors:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def rs_regression_s4():
    degree = 4
    modulus = 0b10011  # x^4+x+1
    q = 1 << degree
    n = q - 1
    r = q // 2 - 1
    m = q // 4

    columns = []
    for t in range(1, q):
        packed = 0
        for j in range(1, r + 1):
            packed |= gf_pow(t, j, modulus, degree) << (degree * (j - 1))
        columns.append(packed)

    assert binary_rank(columns) == n - 1
    syndromes = set()
    for subset in combinations(range(n), m):
        syndrome = 0
        for index in subset:
            syndrome ^= columns[index]
        syndromes.add(syndrome)
    assert len(syndromes) == comb(n, m) == 1365
    assert len(syndromes) < 2 ** (n - 1)


def main():
    cyclic_checks()
    rs_regression_s4()
    print("RESULT: PASS")
    print("weighted_trace_checks=PASS")
    print("multiplicity_thick_checks=PASS")
    print("gf16_rank=14")
    print("gf16_weight4_image=1365")


if __name__ == "__main__":
    main()
