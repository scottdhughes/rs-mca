#!/usr/bin/env python3
"""Exact replay for the dense-shell all-K root-toggle packet.

The mathematical proof is termwise.  This verifier exercises the compiler
interfaces with exact Fraction arithmetic, checks the no-carry class split and
the repaired charge formulas, binds the public theorem statements to source
markers, and provides fail-closed mutations.  No floating grid is used.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "experimental/notes/thresholds/dense_shell_general_k_root_anchor.md"
LEAN = (
    ROOT
    / "experimental/lean/dense_shell_general_k_root_anchor/"
    / "DenseShellGeneralKRootAnchor.lean"
)

FAILED: list[str] = []
PASSED = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASSED
    if ok:
        PASSED += 1
    else:
        FAILED.append(name)
    suffix = f" ({detail})" if detail else ""
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def subsets(values: tuple[int, ...]):
    for size in range(len(values) + 1):
        yield from combinations(values, size)


def valid_base_support(B: int, support: tuple[int, ...], tamper: str | None) -> bool:
    valid = (
        B >= 2
        and len(set(support)) == len(support)
        and all(0 <= index <= B - 2 for index in support)
    )
    if tamper == "boundary-domain" and B == 4 and B - 1 in support:
        return True
    if tamper == "empty-base" and B == 2 and support == ():
        return False
    return valid


def scan_states(word: tuple[int, ...]) -> tuple[Fraction, ...]:
    state = Fraction(0)
    states = []
    for digit in word:
        state = (Fraction(digit) + state) / 3
        states.append(state)
    return tuple(states)


def a_model(state: Fraction) -> Fraction:
    """Even exact profile with the source root value a(+/-1/3)=3/4.

    Later levels are deliberately generic.  The proof uses only evenness and
    the first-level value; this model is a regression fixture, not evidence
    for an analytic estimate.
    """

    return Fraction(1, 2) + Fraction(9, 4) * state * state


def q_model(state: Fraction, position: int, tamper: str | None) -> Fraction:
    value = a_model(state) - Fraction(1, 2)
    if tamper == "root-factor" and position == 1:
        return Fraction(1, 5)
    return value


def poly_mul(left: tuple[Fraction, ...], right: tuple[Fraction, ...]):
    out = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return tuple(out)


def poly_add(left: tuple[Fraction, ...], right: tuple[Fraction, ...]):
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    )


def poly_scale(scale: Fraction, poly: tuple[Fraction, ...]):
    return tuple(scale * value for value in poly)


def root_poly(states: tuple[Fraction, ...], start: int = 0):
    out = (Fraction(1),)
    for state in states[start:]:
        out = poly_mul(out, (-a_model(state), Fraction(1)))
    return out


def decorated_cascade(B: int, K: tuple[int, ...], tamper: str | None = None):
    out = (Fraction(0),)
    for word in product((-1, 1), repeat=B):
        states = scan_states(word)
        decoration = Fraction(1)
        for position in K:
            decoration *= q_model(states[position - 1], position, tamper)
        out = poly_add(out, poly_scale(decoration, root_poly(states)))
    return out


def poly_eval(poly: tuple[Fraction, ...], x: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in reversed(poly):
        value = value * x + coefficient
    return value


def prefix_terms(B: int, K: tuple[int, ...], tamper: str | None = None):
    first = min(K)
    x = Fraction(2, 7)
    terms = []
    for prefix in product((-1, 1), repeat=first - 1):
        prefix_states = scan_states(prefix)
        prefix_poly = root_poly(prefix_states)
        suffix_sum = (Fraction(0),)
        for suffix in product((-1, 1), repeat=B - first + 1):
            word = prefix + suffix
            states = scan_states(word)
            decoration = Fraction(1)
            for position in K:
                decoration *= q_model(states[position - 1], position, tamper)
            suffix_sum = poly_add(
                suffix_sum,
                poly_scale(decoration, root_poly(states, first - 1)),
            )
        term = poly_eval(prefix_poly, x) * poly_eval(suffix_sum, x)
        if B % 2:
            term = -term
        terms.append(term)
    return terms


def weight(word: tuple[int, ...]) -> Fraction:
    states = scan_states(word)
    return Fraction(1) + sum((state * state for state in states), Fraction(0))


def moment(B: int, K: tuple[int, ...], tamper: str | None = None) -> Fraction:
    total = Fraction(0)
    for word in product((-1, 1), repeat=B):
        states = scan_states(word)
        decoration = Fraction(1)
        for position in K:
            decoration *= q_model(states[position - 1], position, tamper)
        total += weight(word) * decoration
    return total


def support_to_scan(B: int, support: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(B - index for index in support))


def class_sigma(B: int, support: tuple[int, ...], tamper: str | None = None):
    K = support_to_scan(B, support)
    return Fraction((-4) ** len(support)) * moment(B, K, tamper)


def support_class(B: int, support: tuple[int, ...]) -> set[int]:
    out = set()
    for signs in product((-1, 1), repeat=len(support)):
        out.add(sum(sign * (3**index) for sign, index in zip(signs, support)))
    return out


def eisenstein_add(left: tuple[int, int], right: tuple[int, int]):
    """Add coefficients in Z[zeta]/(zeta^2+zeta+1)."""

    return left[0] + right[0], left[1] + right[1]


def zeta_power(exponent: int) -> tuple[int, int]:
    residue = exponent % 3
    if residue == 0:
        return 1, 0
    if residue == 1:
        return 0, 1
    return -1, -1


def positive_mass(values: tuple[Fraction, ...]) -> Fraction:
    return sum((value for value in values if value > 0), Fraction(0))


def absolute_mass(values: tuple[Fraction, ...]) -> Fraction:
    return sum((abs(value) for value in values), Fraction(0))


def wrong_sign_mass(values: tuple[Fraction, ...], predicted: int) -> Fraction:
    return sum(
        (abs(value) for value in values if predicted * value < 0), Fraction(0)
    )


def values_with_sum(size: int, target: Fraction) -> tuple[Fraction, ...]:
    if size == 1:
        return (target,)
    prefix = tuple(Fraction(((-1) ** i) * (i + 1), 7) for i in range(size - 1))
    return prefix + (target - sum(prefix, Fraction(0)),)


def gate_sources(tamper: str | None) -> bool:
    if tamper == "source-marker":
        return False
    note = NOTE.read_text(encoding="utf-8")
    lean = LEAN.read_text(encoding="utf-8")
    note_markers = (
        "Theorem 2.1 (all-K decorated root toggle)",
        "Sigma_U = -Sigma_V",
        "Omega_U + Omega_V = (M_U+M_V)/2",
        "There is no convention for an input `V` that already contains `B-1`",
        "chi_4(-3) = zeta",
        "Full C3 restoration still requires the named P7",
        "The theorem does not consume or upgrade the P11",
    )
    lean_markers = (
        "theorem constant_decoration_deletion",
        "theorem paired_class_sums_cancel",
        "theorem paired_positive_charge_cleared",
    )
    return all(marker in note for marker in note_markers) and all(
        marker in lean for marker in lean_markers
    )


def run(tamper: str | None = None) -> bool:
    print("INPUT: decorated B<=8; class split B<=10; exact rational/integer arithmetic")
    print("OBJECT: all-K root toggle, prefix partition, top-support pairing")
    print("THEOREM: dense-shell-general-k-root-anchor")
    print("STATUS: PROVED (finite replay is regression only)")

    root_ok = True
    for digit in (-1, 1):
        state = scan_states((digit,))[0]
        root_ok &= state in (Fraction(-1, 3), Fraction(1, 3))
        root_ok &= q_model(state, 1, tamper) == Fraction(1, 4)
    check("G1 exact root state and q1=1/4", root_ok)

    cascade_cases = 0
    cascade_ok = True
    for B in range(1, 9):
        for K in subsets(tuple(range(2, B + 1))):
            cascade_cases += 1
            left = decorated_cascade(B, tuple(sorted((1,) + K)), tamper)
            right = poly_scale(Fraction(1, 4), decorated_cascade(B, K, tamper))
            cascade_ok &= left == right
    check(
        "G2 coefficientwise root-toggle for every K through B=8",
        cascade_ok,
        f"cases={cascade_cases}",
    )

    prefix_cases = 0
    prefix_ok = True
    for B in range(2, 9):
        for K in subsets(tuple(range(2, B + 1))):
            if not K:
                continue
            prefix_cases += 1
            anchored = decorated_cascade(B, tuple(sorted((1,) + K)), tamper)
            lhs = poly_eval(anchored, Fraction(2, 7))
            if B % 2:
                lhs = -lhs
            rhs = Fraction(1, 4) * sum(prefix_terms(B, K, tamper), Fraction(0))
            prefix_ok &= lhs == rhs
    check(
        "G3 C3b root-anchor prefix partition for every K through B=8",
        prefix_ok,
        f"cases={prefix_cases}",
    )

    boundary_cases = 0
    boundary_ok = True
    for B in (2, 3, 4):
        top = 3 ** (B - 1)
        for V in subsets(tuple(range(B - 1))):
            boundary_cases += 1
            boundary_ok &= valid_base_support(B, V, tamper)
            U = tuple(sorted(V + (B - 1,)))
            class_v = support_class(B, V)
            class_u = support_class(B, U)
            boundary_top = (
                top + 1 if tamper == "minimal-depth" and B == 2 and V == () else top
            )
            expected = {value - boundary_top for value in class_v} | {
                value + boundary_top for value in class_v
            }
            boundary_ok &= class_u == expected
        boundary_ok &= valid_base_support(B, (), tamper)
        boundary_ok &= not valid_base_support(B, (B - 1,), tamper)
    witness_v = support_class(4, (0,))
    witness_u = support_class(4, (0, 3))
    boundary_ok &= witness_v == {-1, 1}
    boundary_ok &= witness_u == {-28, -26, 26, 28}
    check(
        "G4 explicit boundary domain: empty V, B=2/3/4, reject top in V",
        boundary_ok,
        f"valid_cases={boundary_cases}; B4_V0={sorted(witness_v)}",
    )

    class_split_cases = 0
    class_split_ok = True
    for B in range(2, 11):
        top = 3 ** (B - 1)
        for V in subsets(tuple(range(B - 1))):
            class_split_cases += 1
            class_split_ok &= valid_base_support(B, V, tamper)
            U = tuple(sorted(V + (B - 1,)))
            class_u = support_class(B, U)
            class_v = support_class(B, V)
            expected = {value - top for value in class_v} | {
                value + top for value in class_v
            }
            class_split_ok &= class_u == expected
            class_split_ok &= len(class_u) == 2 * len(class_v)
    check(
        "G5 no-carry top-support class decomposition through B=10",
        class_split_ok,
        f"cases={class_split_cases}",
    )

    dense_b2 = {
        (d0 + 3 * d1) % 9 for d0, d1 in product((-1, 1), repeat=2)
    }
    literal_xi = 4
    if tamper == "fourier-sign":
        minus_atom = zeta_power(-literal_xi)
        plus_atom = zeta_power(literal_xi)
    else:
        minus_atom = zeta_power(literal_xi)
        plus_atom = zeta_power(-literal_xi)
    center_atom = zeta_power(0)
    atom_sum = eisenstein_add(eisenstein_add(minus_atom, center_atom), plus_atom)
    fourier_literal_ok = (
        dense_b2 == {2, 4, 5, 7}
        and minus_atom == (0, 1)
        and center_atom == (1, 0)
        and plus_atom == (-1, -1)
        and atom_sum == (0, 0)
    )
    check(
        "G6 B=2 Fourier-sign literal chi_4(-3),chi_4(0),chi_4(3)",
        fourier_literal_ok,
        f"atoms={minus_atom},{center_atom},{plus_atom}",
    )

    sigma_cases = 0
    sigma_ok = True
    for B in range(2, 9):
        for V in subsets(tuple(range(B - 1))):
            sigma_cases += 1
            U = tuple(sorted(V + (B - 1,)))
            sigma_u = class_sigma(B, U, tamper)
            sigma_v = class_sigma(B, V, tamper)
            sigma_ok &= sigma_u == -sigma_v
            s_v = -1 if (B - len(V)) % 2 else 1
            s_u = -1 if (B - len(U)) % 2 else 1
            sigma_ok &= s_u * sigma_u == s_v * sigma_v
    check(
        "G7 C1 class-sum antisymmetry and sign-margin preservation",
        sigma_ok,
        f"cases={sigma_cases}",
    )

    b4_v0 = class_sigma(4, (0,), tamper)
    b4_u03 = class_sigma(4, (0, 3), tamper)
    if tamper == "boundary-sign":
        b4_u03 = -b4_u03
    boundary_sigma_ok = b4_u03 == -b4_v0
    for singleton in ((0,), (1,), (2,)):
        paired = tuple(sorted(singleton + (3,)))
        singleton_sigma = class_sigma(4, singleton, tamper)
        boundary_sigma_ok &= singleton_sigma != 0
        boundary_sigma_ok &= class_sigma(4, paired, tamper) == -singleton_sigma
    check(
        "G8 B=4 exact-model singleton boundary, #914-analogue V={0}",
        boundary_sigma_ok,
        f"singletons=3 nonzero; model_Sigma_V0={b4_v0}",
    )

    charge_supports = 0
    charge_fixtures = 0
    charge_ok = True
    for B in range(2, 9):
        for V in subsets(tuple(range(B - 1))):
            charge_supports += 1
            s_v = -1 if (B - len(V)) % 2 else 1
            s_u = -s_v
            for orientation in (1, -1):
                charge_fixtures += 1
                target_v = Fraction(orientation * s_v * (len(V) + 2), 3)
                target_u = -target_v
                vals_v = values_with_sum(2 ** len(V), target_v)
                vals_u = values_with_sum(2 ** (len(V) + 1), target_u)
                sigma_v = sum(vals_v, Fraction(0))
                sigma_u = sum(vals_u, Fraction(0))
                mass_v = absolute_mass(vals_v)
                mass_u = absolute_mass(vals_u)
                omega_v = positive_mass(vals_v)
                omega_u = positive_mass(vals_u)
                wrong_v = wrong_sign_mass(vals_v, s_v)
                wrong_u = wrong_sign_mass(vals_u, s_u)
                correction = s_v * sigma_v
                if tamper == "charge-correction":
                    correction = -correction
                charge_ok &= sigma_u == -sigma_v
                charge_ok &= 2 * (omega_u + omega_v) == mass_u + mass_v
                charge_ok &= (
                    2 * (wrong_u + wrong_v)
                    == mass_u + mass_v - 2 * s_v * sigma_v
                )
                charge_ok &= omega_u + omega_v == wrong_u + wrong_v + correction
                if orientation == 1:
                    charge_ok &= correction == abs(sigma_v)
                else:
                    charge_ok &= correction == -abs(sigma_v)
    check(
        "G9 repaired charge pair; |Sigma| only on sign-aligned fixtures",
        charge_ok,
        f"supports={charge_supports}; aligned/opposed_fixtures={charge_fixtures}",
    )

    source_ok = gate_sources(tamper)
    check("G10 required source markers present in note and Lean declarations", source_ok)

    total = PASSED + len(FAILED)
    print(f"CERTIFICATE: exact checks={PASSED}/{total}; deterministic seed=none")
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} ({PASSED}/{total})")
    return not FAILED


def tamper_selftest() -> bool:
    tampers = (
        "root-factor",
        "empty-base",
        "boundary-domain",
        "minimal-depth",
        "fourier-sign",
        "boundary-sign",
        "charge-correction",
        "source-marker",
    )
    runs = [
        (
            tamper,
            subprocess.Popen(
                [sys.executable, __file__, "--tamper", tamper],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            ),
        )
        for tamper in tampers
    ]
    caught = 0
    for tamper, process in runs:
        stdout, _ = process.communicate()
        detected = process.returncode != 0 and "RESULT: FAIL" in stdout
        caught += int(detected)
        print(f"tamper {tamper}: {'caught' if detected else 'MISSED'}")
    print(f"TAMPER SELFTEST: {caught}/{len(tampers)} caught")
    return caught == len(tampers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tamper",
        choices=(
            "root-factor",
            "empty-base",
            "boundary-domain",
            "minimal-depth",
            "fourier-sign",
            "boundary-sign",
            "charge-correction",
            "source-marker",
        ),
    )
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return 0 if tamper_selftest() else 1
    return 0 if run(args.tamper) else 1


if __name__ == "__main__":
    raise SystemExit(main())
