#!/usr/bin/env python3
"""Exact verifier for the KoalaBear source-bound shortening adapter."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank11-source-bound-shortening-v1/result.json"
NESTED = ROOT / "experimental/data/certificates/kb-mca-rank11-nested-pinned-span-ladder-v1/result.json"

PARENT = "42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08"
BASE1173 = "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
N, K, M = 2_097_152, 1_048_576, 1_116_048
LOADS = [
    2_843_853_816_476_423,
    93_708_171_878_891,
    3_087_708_134_499,
    101_738_094_101,
    3_352_119_806,
    110_444_488,
    3_638_792,
    119_884,
    3_950,
    131,
]
DIMS = [8, 7, 6, 5, 3, 2, 2, 2, 2, 2]


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def poly_eval(coeffs: list[int], x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(coeffs):
        value = (value * x + coefficient) % p
    return value


def poly_add(a: list[int], b: list[int], p: int) -> list[int]:
    length = max(len(a), len(b))
    out = [0] * length
    for i in range(length):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_div_exact(numerator: list[int], denominator: list[int], p: int) -> list[int]:
    num = numerator[:]
    while len(num) > 1 and num[-1] == 0:
        num.pop()
    den = denominator[:]
    while len(den) > 1 and den[-1] == 0:
        den.pop()
    require(den[-1] % p != 0, "nonzero denominator leading coefficient")
    inverse = pow(den[-1], -1, p)
    quotient = [0] * max(1, len(num) - len(den) + 1)
    while len(num) >= len(den) and any(num):
        shift = len(num) - len(den)
        factor = num[-1] * inverse % p
        quotient[shift] = factor
        for j in range(len(den)):
            num[shift + j] = (num[shift + j] - factor * den[j]) % p
        while len(num) > 1 and num[-1] == 0:
            num.pop()
    require(all(x % p == 0 for x in num), "exact polynomial division")
    while len(quotient) > 1 and quotient[-1] == 0:
        quotient.pop()
    return quotient


def affine_matches(values: list[int], points: list[int], p: int) -> bool:
    for a in range(p):
        for b in range(p):
            if all((a + b * x) % p == values[x] for x in points):
                return True
    return False


def finite_support_replacement_control() -> dict[str, Any]:
    p = 5
    r1 = [0, 0, 1, 0]
    original = [0, 1, 2]
    replacement = [0, 1, 3]
    complete = [0, 1, 2, 3]
    require(not affine_matches(r1, original, p), "original support pair-noncontained")
    require(affine_matches(r1, replacement, p), "replacement support becomes pair-contained")
    require(not affine_matches(r1, complete, p), "complete domain remains pair-noncontained")

    # Shorten the complete domain at T={3}.  The interpolation word is zero and
    # the locator is X-3.  The shortened r1 values on 0,1,2 are divided
    # coordinatewise by the nonzero locator.
    shortened = [(r1[x] * pow((x - 3) % p, -1, p)) % p for x in original]
    require(len(set(shortened)) > 1, "shortened K'=1 pair remains noncontained")
    return {
        "field": p,
        "original_pair_noncontained": True,
        "replacement_pair_contained": True,
        "complete_pair_noncontained": True,
        "shortened_values": shortened,
    }


def finite_locator_bijection_control() -> dict[str, Any]:
    p = 5
    # T={0,1}, K=3.  Fix interpolation values f(0)=2, f(1)=4.
    interp = [2, 2]  # 2+2X
    locator = [0, -1 % p, 1]  # X(X-1)
    images = []
    for q in range(p):
        f = poly_add(interp, poly_mul(locator, [q], p), p)
        require(len(f) <= 3, "lift degree <3")
        require(poly_eval(f, 0, p) == 2 and poly_eval(f, 1, p) == 4, "interpolation values")
        recovered = poly_div_exact(poly_add(f, [(-x) % p for x in interp], p), locator, p)
        require(recovered == [q], "quotient recovery")
        images.append(tuple(f + [0] * (3 - len(f))))

    exhaustive = []
    for a in range(p):
        for b in range(p):
            for c in range(p):
                f = [a, b, c]
                if poly_eval(f, 0, p) == 2 and poly_eval(f, 1, p) == 4:
                    exhaustive.append(tuple(f))
    require(sorted(images) == sorted(exhaustive), "shortening quotient/lift bijection")
    return {"field": p, "constrained_codewords": len(exhaustive), "expected": p}


def build() -> dict[str, Any]:
    nested = json.loads(NESTED.read_text())
    inherited_loads = [nested["nested_loads"][str(k)] for k in range(1, 11)]
    inherited_dims = [nested["dimension_floors"][str(k)] for k in range(1, 11)]
    require(inherited_loads == LOADS, "inherited loads")
    require(inherited_dims == DIMS, "inherited dimensions")

    rows = []
    for k, (load, dimension) in enumerate(zip(LOADS, DIMS), 1):
        row = {
            "k": k,
            "n": N - k,
            "K": K - k,
            "m": M - k,
            "n_minus_K": N - K,
            "m_minus_K": M - K,
            "n_minus_m": N - M,
            "degree_ceiling": K - k,
            "slope_load": load,
            "dimension_floor": dimension,
        }
        require(row["n_minus_K"] == 1_048_576, "n-K invariant")
        require(row["m_minus_K"] == 67_472, "m-K invariant")
        require(row["n_minus_m"] == 981_104, "n-m invariant")
        rows.append(row)

    return {
        "schema": "kb-mca-rank11-source-bound-shortening-v1",
        "parent": PARENT,
        "base_pr1173_head": BASE1173,
        "nested_result_source": "experimental/data/certificates/kb-mca-rank11-nested-pinned-span-ladder-v1/result.json",
        "shortened_rows": rows,
        "support_replacement_counterexample": {
            "field": 5,
            "domain": [0, 1, 2, 3],
            "K": 2,
            "m": 3,
            "slope": 0,
            "r0": [0, 0, 0, 0],
            "r1": [0, 0, 1, 0],
            "original_support": [0, 1, 2],
            "replacement_support": [0, 1, 3],
            "original_pair_noncontained": True,
            "replacement_pair_contained": True,
            "complete_domain": [0, 1, 2, 3],
            "shortening_set": [3],
            "shortened_bad_domain": [0, 1, 2],
        },
        "finite_controls": {
            "support_replacement": finite_support_replacement_control(),
            "locator_bijection": finite_locator_bijection_control(),
        },
        "claims": {
            "complete_agreement_shortening_proved": True,
            "nested_source_bound_shortening_proved": True,
            "compatible_quotient_ladder_proved": True,
            "rank11_paid": False,
            "koalabear_closed": False,
            "active_v4_ledger_movement": 0,
        },
    }


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = [
        ("parent", None, BASE1173),
        ("shortened_rows", 0, {**expected["shortened_rows"][0], "m": M}),
        ("shortened_rows", 3, {**expected["shortened_rows"][3], "slope_load": LOADS[3] - 1}),
        ("shortened_rows", 9, {**expected["shortened_rows"][9], "dimension_floor": 1}),
        ("claims", "rank11_paid", True),
        ("claims", "koalabear_closed", True),
        ("support_replacement_counterexample", "replacement_pair_contained", False),
        ("support_replacement_counterexample", "complete_domain", [0, 1, 3]),
    ]
    caught = 0
    for section, key, value in mutations:
        changed = copy.deepcopy(expected)
        if section == "parent":
            changed["parent"] = value
        elif section == "shortened_rows":
            changed[section][key] = value
        else:
            changed[section][key] = value
        try:
            require(changed == expected, "canonical result")
        except Reject:
            caught += 1
    require(caught == len(mutations), "all hostile mutations caught")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    expected = build()
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {RESULT}")
        return

    actual = json.loads(RESULT.read_text())
    require(actual == expected, "result certificate")

    if args.tamper_selftest:
        caught = tamper_selftest(expected)
        print(f"KB_MCA_RANK11_SOURCE_SHORTENING_TAMPER_PASS mutations={caught}/8")
    elif args.json:
        print(json.dumps(expected, sort_keys=True, separators=(",", ":")))
    else:
        print(
            "KB_MCA_RANK11_SOURCE_SHORTENING_PASS "
            f"rows={len(actual['shortened_rows'])} "
            f"load1={actual['shortened_rows'][0]['slope_load']} "
            f"dim1={actual['shortened_rows'][0]['dimension_floor']} "
            f"lift_controls={actual['finite_controls']['locator_bijection']['constrained_codewords']}"
        )


if __name__ == "__main__":
    main()
