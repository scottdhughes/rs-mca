#!/usr/bin/env python3
"""Fail-closed replay for the fixed-26 direct eliminant theorem."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from itertools import permutations
from pathlib import Path
from typing import Any, Callable, Iterable


class VerificationError(RuntimeError):
    """Raised when a pinned theorem or replay check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError("CHECK FAILED: " + message)


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
CERT_REL = "experimental/data/certificates/rank16-fixed26-direct-eliminant"
CERT_DIR = REPO_ROOT / CERT_REL
MANIFEST_PATH = CERT_DIR / "manifest.json"
EXPECTED_PATH = CERT_DIR / "verify_rank16_fixed26_direct_eliminant.expected.txt"
CHECKSUM_PATH = CERT_DIR / "SHA256SUMS"

NOTE_REL = "experimental/notes/l2/rank16_fixed26_direct_eliminant.md"
SCRIPT_REL = "experimental/scripts/verify_rank16_fixed26_direct_eliminant.py"
MANIFEST_REL = CERT_REL + "/manifest.json"
EXPECTED_REL = CERT_REL + "/verify_rank16_fixed26_direct_eliminant.expected.txt"
ARTIFACTS = (NOTE_REL, SCRIPT_REL, MANIFEST_REL, EXPECTED_REL)

SCHEMA = "rs-mca.rank16-fixed26-direct-eliminant.v1"
BASE = "3404d21b64c876c6d9b995ad3e29d7120ab27a54"
AUDIT_PACKET_SHA256 = "d981b84c7c7e3f82ee1abb4e1fd3458b3fcd0e3d2027f312f9986600022cf28f"
AUDIT_CLEAN_SHA256 = "72b65f8a994668699bcc87c97fbdf35db8d9b0ee8a93df0a470c43335810f947"
SOURCE_PINS = {
    "experimental/notes/l2/rank16_fixed26_divided_difference_source_compiler.md":
        "e508b1847228475e5a71ab12df15d69d4091e7558a91f53e68261f06c42205ab",
    "experimental/scripts/verify_rank16_fixed26_divided_difference_source_compiler.py":
        "2dd8cd4d2df24510a4faa57d4ad70feda1b4505814233547f06dea7293afc744",
    "experimental/notes/l2/rank16_fixed26_polynomial_cross_minor_lift.md":
        "a8828bffa507b56ebc9795d9c2badc904a24df02ecbbd980faef1eafa28b81ea",
    "experimental/scripts/verify_rank16_fixed26_polynomial_cross_minor_lift.py":
        "1a5bec7dd8aefb8079c7cfa5e9d5b732c57e2365adfa94a8e5e28e12c6d2a86e",
    "experimental/notes/l2/rank16_fixed26_spectral_resolvent.md":
        "3c8aaddaa9993cb486d918c62101938f9c7bf4604a852863778f0ccd6886f0cd",
    "experimental/scripts/verify_rank16_fixed26_spectral_resolvent.py":
        "1327c517be7d87050785980b2780bbd99862e6de71e50d188b2a353706336014",
    "experimental/notes/l2/rank16_fixed26_global_spectral_rank_gap.md":
        "4d212b4dd1821cefb3866f67a6303e034be88e7ade3b57bd941aedb93e32dcdb",
    "experimental/scripts/verify_rank16_fixed26_global_spectral_rank_gap.py":
        "37a26c742f09b271f567c2a000810e15cd904ad7f301ff538679766980e0a53d",
}

PolyX = tuple[int, ...]
PolyZ = tuple[PolyX, ...]
ZERO_X: PolyX = ()
ONE_X: PolyX = (1,)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_manifest() -> dict[str, Any]:
    try:
        value = json.loads(
            MANIFEST_PATH.read_text(encoding="ascii"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError("cannot read strict ASCII manifest") from exc
    require(type(value) is dict, "manifest root object")
    return value


def manifest_contract(expected_sha256: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "base": BASE,
        "audit_packet_sha256": AUDIT_PACKET_SHA256,
        "audit_clean_sha256": AUDIT_CLEAN_SHA256,
        "source_pins": SOURCE_PINS,
        "field_and_parameters": {
            "field_prime": 2_130_706_433,
            "domain_order": 2_097_152,
            "block_size_b": 32_768,
            "generator_degree_a": 67_472,
            "residual_degree_r": 63_601,
            "adjacent_gcd_degree_d": 28_897,
            "cofactor_quotient_degree_L3": 59_730,
            "scalar_group_order": 64,
        },
        "source_contract": {
            "fixed_received_word_and_first_match_owner": True,
            "nonzero_eta_then_canonical_xi": True,
            "fixed_core_labels": 26,
            "external_labels": 8,
            "actual_valid_cross_edges": 16,
            "source_normalized_entries": True,
            "rank_field": "F_p(X)",
            "all_3x3_cross_minors_zero": True,
            "nonzero_2x2_gap": 5_807,
        },
        "sylvester_convention": {
            "first_block": "v shifted descending-coefficient rows of P",
            "second_block": "u shifted descending-coefficient rows of Q",
            "columns": "descending powers Z^(u+v-1) through 1",
            "formal_degree_zero_padding": True,
            "resultant_uses_same_exact_degree_convention": True,
        },
        "theorem": {
            "transfer_degrees": [2, 3],
            "A_degree": "m-1",
            "E_degree_at_most": "m",
            "J_degree_caps": {"2": 30_831, "3": 57_794},
            "M_may_be_zero": True,
            "repeated_generator_factors_allowed": True,
            "M_degree_caps_when_nonzero": {"2": 100_237, "3": 133_003},
            "quadratic_scalar_roots": 0,
            "cubic_scalar_roots_at_most": 1,
            "cubic_scalar_root_simple": True,
            "valuation_zero_convention": "v_pi(0)=+infinity",
        },
        "nonclaims": {
            "terminal_closure": False,
            "M_nonzero": False,
            "source_locator_divides_M": False,
            "strict_valuation_excess": False,
            "owner_payment": False,
            "finite_payment": False,
            "asymptotic_payment": False,
            "grand_list": False,
            "grand_mca": False,
            "score_movement": False,
        },
        "remaining_wall": (
            "derive a source-incidence divisor of M or classify M=0 strongly "
            "enough to exclude both transfer degrees"
        ),
        "expected_output": {"path": EXPECTED_REL, "sha256": expected_sha256},
        "artifacts": list(ARTIFACTS),
    }


def validate_manifest(value: dict[str, Any]) -> None:
    output = value.get("expected_output")
    require(type(output) is dict, "expected output object")
    digest = output.get("sha256")
    require(
        type(digest) is str and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
        "expected output SHA-256",
    )
    require(value == manifest_contract(digest), "semantic manifest contract")


def verify_source_pins() -> int:
    for relative, digest in SOURCE_PINS.items():
        path = (REPO_ROOT / relative).resolve()
        require(REPO_ROOT in path.parents, "source pin confinement")
        require(path.is_file(), "source pin exists: " + relative)
        require(sha256_path(path) == digest, "source pin digest: " + relative)
    return len(SOURCE_PINS)


def verify_artifacts(manifest: dict[str, Any]) -> int:
    raw = CHECKSUM_PATH.read_bytes()
    require(raw.endswith(b"\n"), "checksum final newline")
    lines = raw.decode("ascii").splitlines()
    require(len(lines) == len(ARTIFACTS), "checksum entry count")
    pattern = re.compile(r"([0-9a-f]{64})  ([!-~]+)")
    for line, expected_relative in zip(lines, ARTIFACTS):
        match = pattern.fullmatch(line)
        require(match is not None, "checksum syntax")
        digest, relative = match.groups()
        require(relative == expected_relative, "checksum order")
        require(sha256_path(REPO_ROOT / relative) == digest, "artifact digest")
    require(tuple(manifest["artifacts"]) == ARTIFACTS, "artifact manifest order")
    require(manifest["expected_output"]["path"] == EXPECTED_REL, "expected path")
    require(
        sha256_path(EXPECTED_PATH) == manifest["expected_output"]["sha256"],
        "expected output digest",
    )
    return len(lines)


def px(values: Iterable[int], prime: int) -> PolyX:
    result = [value % prime for value in values]
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def px_degree(value: PolyX) -> int:
    return len(value) - 1


def px_add(left: PolyX, right: PolyX, prime: int) -> PolyX:
    size = max(len(left), len(right))
    return px(
        ((left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)
         for i in range(size)),
        prime,
    )


def px_neg(value: PolyX, prime: int) -> PolyX:
    return px((-item for item in value), prime)


def px_sub(left: PolyX, right: PolyX, prime: int) -> PolyX:
    return px_add(left, px_neg(right, prime), prime)


def px_scale(value: PolyX, scalar: int, prime: int) -> PolyX:
    return px((scalar * item for item in value), prime)


def px_mul(left: PolyX, right: PolyX, prime: int) -> PolyX:
    if not left or not right:
        return ZERO_X
    result = [0] * (len(left) + len(right) - 1)
    for i, a_value in enumerate(left):
        for j, b_value in enumerate(right):
            result[i + j] = (result[i + j] + a_value * b_value) % prime
    return px(result, prime)


def px_pow(value: PolyX, exponent: int, prime: int) -> PolyX:
    require(exponent >= 0, "nonnegative polynomial exponent")
    result = ONE_X
    base = value
    power = exponent
    while power:
        if power & 1:
            result = px_mul(result, base, prime)
        base = px_mul(base, base, prime)
        power //= 2
    return result


def px_divmod(numerator: PolyX, denominator: PolyX, prime: int) -> tuple[PolyX, PolyX]:
    require(bool(denominator), "nonzero polynomial denominator")
    remainder = list(numerator)
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    inverse_lead = pow(denominator[-1], prime - 2, prime)
    while remainder and len(remainder) >= len(denominator):
        shift = len(remainder) - len(denominator)
        factor = remainder[-1] * inverse_lead % prime
        quotient[shift] = factor
        for index, coefficient in enumerate(denominator):
            remainder[shift + index] = (
                remainder[shift + index] - factor * coefficient
            ) % prime
        while remainder and remainder[-1] == 0:
            remainder.pop()
    return px(quotient, prime), px(remainder, prime)


def px_exact_quotient(numerator: PolyX, denominator: PolyX, prime: int) -> PolyX:
    quotient, remainder = px_divmod(numerator, denominator, prime)
    require(not remainder, "exact polynomial quotient")
    return quotient


def px_gcd(left: PolyX, right: PolyX, prime: int) -> PolyX:
    a_value, b_value = left, right
    while b_value:
        _, remainder = px_divmod(a_value, b_value, prime)
        a_value, b_value = b_value, remainder
    if not a_value:
        return ZERO_X
    return px_scale(a_value, pow(a_value[-1], prime - 2, prime), prime)


def x_power(exponent: int) -> PolyX:
    return (0,) * exponent + (1,)


def pz(values: Iterable[PolyX]) -> PolyZ:
    result = list(values)
    while result and not result[-1]:
        result.pop()
    return tuple(result)


def pz_degree(value: PolyZ) -> int:
    return len(value) - 1


def pz_coeff(value: PolyZ, index: int) -> PolyX:
    return value[index] if 0 <= index < len(value) else ZERO_X


def pz_add(left: PolyZ, right: PolyZ, prime: int) -> PolyZ:
    size = max(len(left), len(right))
    return pz(px_add(pz_coeff(left, i), pz_coeff(right, i), prime) for i in range(size))


def pz_neg(value: PolyZ, prime: int) -> PolyZ:
    return pz(px_neg(item, prime) for item in value)


def pz_sub(left: PolyZ, right: PolyZ, prime: int) -> PolyZ:
    return pz_add(left, pz_neg(right, prime), prime)


def pz_mul(left: PolyZ, right: PolyZ, prime: int) -> PolyZ:
    if not left or not right:
        return ()
    result = [ZERO_X] * (len(left) + len(right) - 1)
    for i, a_value in enumerate(left):
        for j, b_value in enumerate(right):
            result[i + j] = px_add(
                result[i + j], px_mul(a_value, b_value, prime), prime
            )
    return pz(result)


def pz_scale_px(value: PolyZ, scalar: PolyX, prime: int) -> PolyZ:
    return pz(px_mul(item, scalar, prime) for item in value)


def pz_eval(value: PolyZ, point: PolyX, prime: int) -> PolyX:
    result = ZERO_X
    for coefficient in reversed(value):
        result = px_add(px_mul(result, point, prime), coefficient, prime)
    return result


def pz_mod_coefficients(value: PolyZ, modulus: PolyX, prime: int) -> PolyZ:
    residues = []
    for coefficient in value:
        _, remainder = px_divmod(coefficient, modulus, prime)
        residues.append(remainder)
    return pz(residues)


def permutation_sign(value: tuple[int, ...]) -> int:
    inversions = sum(
        value[i] > value[j]
        for i in range(len(value))
        for j in range(i + 1, len(value))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[PolyX]], prime: int) -> PolyX:
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "square determinant matrix")
    result = ZERO_X
    for choice in permutations(range(size)):
        term = ONE_X
        for row, column in enumerate(choice):
            term = px_mul(term, matrix[row][column], prime)
        if permutation_sign(choice) < 0:
            term = px_neg(term, prime)
        result = px_add(result, term, prime)
    return result


def sylvester(
    left: PolyZ, right: PolyZ, left_degree: int, right_degree: int, prime: int
) -> PolyX:
    require(pz_degree(left) <= left_degree, "left formal degree")
    require(pz_degree(right) <= right_degree, "right formal degree")
    width = left_degree + right_degree
    left_desc = [pz_coeff(left, i) for i in range(left_degree, -1, -1)]
    right_desc = [pz_coeff(right, i) for i in range(right_degree, -1, -1)]
    rows: list[list[PolyX]] = []
    for shift in range(right_degree):
        rows.append(
            [ZERO_X] * shift
            + left_desc
            + [ZERO_X] * (right_degree - 1 - shift)
        )
    for shift in range(left_degree):
        rows.append(
            [ZERO_X] * shift
            + right_desc
            + [ZERO_X] * (left_degree - 1 - shift)
        )
    require(len(rows) == width, "Sylvester row count")
    return determinant(rows, prime)


def make_f(point: PolyX, prime: int) -> PolyZ:
    return pz((point, px((-1,), prime)))


def general_case(
    m: int,
    g_value: PolyX,
    xi: PolyX,
    point: PolyX,
    k_value: PolyZ,
    j0: PolyX,
    l_value: PolyZ,
    h_value: PolyZ | None,
    prime: int,
) -> dict[str, Any]:
    f_value = make_f(point, prime)
    base_b = pz_add(pz_mul(f_value, k_value, prime), (px_mul(g_value, j0, prime),), prime)
    base_a = pz_add(pz_scale_px(k_value, xi, prime), pz_scale_px(l_value, g_value, prime), prime)
    base_e = pz_sub(pz_mul(f_value, l_value, prime), (px_mul(xi, j0, prime),), prime)
    factor = h_value if h_value is not None else (ONE_X,)
    k_effective = pz_mul(factor, k_value, prime)
    return {
        "m": m,
        "g": g_value,
        "xi": xi,
        "T": point,
        "F": f_value,
        "A": pz_mul(factor, base_a, prime),
        "B": pz_mul(factor, base_b, prime),
        "E": pz_mul(factor, base_e, prime),
        "J": px_mul(pz_eval(factor, point, prime), j0, prime),
        "K": k_effective,
        "zero_resultant": h_value is not None,
        "repeated_g": True,
        "nonconstant_xi": px_degree(xi) > 0,
    }


def replay_cases() -> dict[str, int]:
    prime = 101
    x = x_power(1)
    x2 = x_power(2)
    x3 = x_power(3)
    x7_plus_2 = px_add(x_power(7), (2,), prime)

    sharp_quadratic = {
        "m": 2,
        "g": x7_plus_2,
        "xi": ONE_X,
        "T": x3,
        "F": make_f(x3, prime),
        "A": pz((px_neg(px_mul(x, x3, prime), prime), px_neg(x, prime))),
        "B": pz(((2,), ZERO_X, x)),
        "E": pz((px((-1,), prime),)),
        "J": ONE_X,
        "K": pz((px_neg(px_mul(x, x3, prime), prime), px_neg(x, prime))),
        "zero_resultant": False,
        "repeated_g": False,
        "nonconstant_xi": False,
    }
    sharp_cubic = {
        "m": 3,
        "g": x7_plus_2,
        "xi": ONE_X,
        "T": x3,
        "F": make_f(x3, prime),
        "A": pz((px_neg(px_mul(x3, x3, prime), prime), px_neg(x3, prime), px((-1,), prime))),
        "B": pz((px_scale(x2, 2, prime), ZERO_X, ZERO_X, ONE_X)),
        "E": pz((px_neg(x2, prime),)),
        "J": x2,
        "K": pz((px_neg(px_mul(x3, x3, prime), prime), px_neg(x3, prime), px((-1,), prime))),
        "zero_resultant": False,
        "repeated_g": False,
        "nonconstant_xi": False,
    }

    g2 = px_pow(px_sub(x, (3,), prime), 2, prime)
    g3 = px_pow(px_sub(x, (4,), prime), 3, prime)
    xi2 = px_add(x, (1,), prime)
    xi3 = px_add(x, (2,), prime)
    repeated_quadratic = general_case(
        2, g2, xi2, x2,
        pz((px_add(x, (2,), prime), ONE_X)),
        px_add(x, (4,), prime), pz(((2,),)), None, prime,
    )
    repeated_cubic = general_case(
        3, g3, xi3, x2,
        pz((px_add(x, (1,), prime), (2,), x)),
        px_add(x, (2,), prime), pz(((3,), ONE_X)), None, prime,
    )
    common_factor = pz((px((-5,), prime), ONE_X))
    zero_quadratic = general_case(
        2, g2, xi2, x2, pz((ONE_X,)), ONE_X, (), common_factor, prime
    )
    zero_cubic = general_case(
        3, g3, xi3, x2, pz((ONE_X, x)), ONE_X, (), common_factor, prime
    )

    cases = (
        sharp_quadratic,
        sharp_cubic,
        repeated_quadratic,
        repeated_cubic,
        zero_quadratic,
        zero_cubic,
    )
    determinant_checks = 0
    local_checks = 0
    for case in cases:
        m = case["m"]
        g_value = case["g"]
        xi = case["xi"]
        a_value = case["A"]
        b_value = case["B"]
        e_value = case["E"]
        j_value = case["J"]
        f_value = case["F"]
        point = case["T"]

        require(px_gcd(g_value, xi, prime) == ONE_X, "g and xi coprime")
        require(pz_degree(a_value) == m - 1, "A exact degree")
        require(pz_degree(b_value) == m, "B exact degree")
        require(pz_degree(e_value) <= m, "E degree")
        relation = pz_sub(
            pz_sub(pz_mul(f_value, a_value, prime), pz_scale_px(b_value, xi, prime), prime),
            pz_scale_px(e_value, g_value, prime),
            prime,
        )
        require(not relation, "eliminant relation")
        require(pz_eval(b_value, point, prime) == px_mul(g_value, j_value, prime), "B(T)=gJ")
        require(pz_eval(e_value, point, prime) == px_neg(px_mul(xi, j_value, prime), prime), "E(T)=-xi J")

        resultant = sylvester(a_value, b_value, m - 1, m, prime)
        g_power = px_pow(g_value, m - 1, prime)
        m_value = px_exact_quotient(resultant, g_power, prime)
        require((not resultant) == case["zero_resultant"], "zero-resultant classification")
        left_companion = sylvester(a_value, e_value, m - 1, m, prime)
        right_companion = sylvester(b_value, e_value, m, m, prime)
        require(
            left_companion == px_mul(px_pow(px_neg(xi, prime), m - 1, prime), m_value, prime),
            "first signed Sylvester companion",
        )
        require(right_companion == px_mul(j_value, m_value, prime), "second signed Sylvester companion")
        determinant_checks += 3

        if case["K"] is not None:
            k_value = case["K"]
            require(
                not pz_mod_coefficients(pz_sub(b_value, pz_mul(f_value, k_value, prime), prime), g_value, prime),
                "local B=F K modulo g",
            )
            require(
                not pz_mod_coefficients(pz_sub(a_value, pz_scale_px(k_value, xi, prime), prime), g_value, prime),
                "local A=xi K modulo g",
            )
        local_checks += 1

    return {
        "cases": len(cases),
        "nonzero": sum(not case["zero_resultant"] for case in cases),
        "zero": sum(case["zero_resultant"] for case in cases),
        "repeated_g": sum(case["repeated_g"] for case in cases),
        "nonconstant_xi": sum(case["nonconstant_xi"] for case in cases),
        "determinant_checks": determinant_checks,
        "local_checks": local_checks,
    }


def verify_deployed_arithmetic() -> None:
    prime = 2_130_706_433
    n = 2_097_152
    b_value = 32_768
    a_value = 67_472
    r_value = 63_601
    d_value = 28_897
    l3_value = 59_730
    require(prime - 1 == (2 ** 24) * 127, "field factorization")
    require((prime - 1) % n == 0, "domain subgroup")
    require(n == 64 * b_value, "64 fibre blocks")
    require(r_value - 2 * d_value == 5_807, "nonzero 2x2 gap")
    require(l3_value == 2 * r_value - a_value, "cofactor quotient degree")
    require(l3_value - b_value == 26_962, "base-T quotient degree")
    require(3 * b_value - 1 - a_value == 30_831, "quadratic J cap")
    require(l3_value + 2 * b_value - a_value == 57_794, "cubic J cap")
    require(2 * (a_value - 1) + (b_value - 1) - a_value == 100_237, "quadratic M cap")
    require(3 * (a_value - 1) + 2 * (b_value - 1) - 2 * a_value == 133_003, "cubic M cap")
    require(30_831 < b_value and 57_794 < 2 * b_value, "strict scalar-fibre endpoints")


def semantic_tamper_selftests(manifest: dict[str, Any]) -> int:
    def alter_base(value: dict[str, Any]) -> None:
        value["base"] = "0" * 40

    def remove_source(value: dict[str, Any]) -> None:
        value["source_pins"].pop(next(iter(value["source_pins"])))

    def reverse_blocks(value: dict[str, Any]) -> None:
        value["sylvester_convention"]["first_block"] = "u rows of Q"

    def reverse_columns(value: dict[str, Any]) -> None:
        value["sylvester_convention"]["columns"] = "ascending powers"

    def alter_cap(value: dict[str, Any]) -> None:
        value["theorem"]["M_degree_caps_when_nonzero"]["3"] = 133_002

    def allow_two_roots(value: dict[str, Any]) -> None:
        value["theorem"]["cubic_scalar_roots_at_most"] = 2

    def exclude_zero(value: dict[str, Any]) -> None:
        value["theorem"]["M_may_be_zero"] = False

    def claim_terminal(value: dict[str, Any]) -> None:
        value["nonclaims"]["terminal_closure"] = True

    def claim_divisor(value: dict[str, Any]) -> None:
        value["nonclaims"]["source_locator_divides_M"] = True

    def claim_score(value: dict[str, Any]) -> None:
        value["nonclaims"]["score_movement"] = True

    mutators: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
        ("base", alter_base),
        ("source pin", remove_source),
        ("row blocks", reverse_blocks),
        ("columns", reverse_columns),
        ("M cap", alter_cap),
        ("scalar roots", allow_two_roots),
        ("zero resultant", exclude_zero),
        ("terminal", claim_terminal),
        ("source divisor", claim_divisor),
        ("score", claim_score),
    )
    rejected = 0
    for name, mutate in mutators:
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        try:
            validate_manifest(candidate)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("semantic tamper accepted: " + name)
    require(rejected == len(mutators), "all semantic tampers rejected")
    return rejected


def render_output(
    source_count: int,
    replay: dict[str, int],
    tamper_count: int,
    artifact_count: int,
) -> bytes:
    lines = (
        "RANK16_FIXED26_DIRECT_ELIMINANT: PASS",
        "schema=" + SCHEMA,
        "base=" + BASE,
        "source_pins=PASS,count=" + str(source_count),
        "deployed=p2130706433,n2097152,b32768,a67472,r63601,d28897,L3_59730",
        (
            "triangle_cases={cases},nonzero={nonzero},zero={zero},"
            "repeated_g={repeated_g},nonconstant_xi={nonconstant_xi}"
        ).format(**replay),
        "sylvester_checks=" + str(replay["determinant_checks"]) + ",local_prime_power_checks=" + str(replay["local_checks"]),
        "degree_caps=M2:100237,M3:133003;J2:30831,J3:57794",
        "scalar_fibres=quadratic:0,cubic:at_most_1_simple",
        "semantic_tamper_selftests=PASS,count=" + str(tamper_count),
        "artifact_checksums=PASS,count=" + str(artifact_count),
        "finite_ledger_delta=0 official_score=0/2",
        "RESULT=PASS",
    )
    return ("\n".join(lines) + "\n").encode("ascii")


def run_default() -> None:
    manifest = load_manifest()
    validate_manifest(manifest)
    source_count = verify_source_pins()
    verify_deployed_arithmetic()
    replay = replay_cases()
    tamper_count = semantic_tamper_selftests(manifest)
    artifact_count = verify_artifacts(manifest)
    output = render_output(source_count, replay, tamper_count, artifact_count)
    require(output == EXPECTED_PATH.read_bytes(), "frozen expected output byte match")
    sys.stdout.buffer.write(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tamper-self-test", action="store_true")
    group.add_argument("--check-checksums", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest()
        validate_manifest(manifest)
        if args.tamper_self_test:
            count = semantic_tamper_selftests(manifest)
            print("SEMANTIC_TAMPER_SELFTESTS: PASS count=" + str(count))
        elif args.check_checksums:
            count = verify_artifacts(manifest)
            print("ARTIFACT_CHECKSUMS: PASS count=" + str(count))
        else:
            run_default()
    except (OSError, UnicodeError, ValueError, VerificationError) as exc:
        print("RANK16_FIXED26_DIRECT_ELIMINANT: FAIL", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
