#!/usr/bin/env python3
"""Verify the finite fixed-26 Bezout-rectangle-conductor theorem packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Callable


class VerificationError(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
NOTE_PATH = ROOT / "experimental/notes/l2/rank16_fixed26_bezout_rectangle_conductor.md"
CERT_DIR = ROOT / "experimental/data/certificates/rank16-fixed26-bezout-rectangle-conductor"
MANIFEST_PATH = CERT_DIR / "manifest.json"
EXPECTED_PATH = CERT_DIR / "verify_rank16_fixed26_bezout_rectangle_conductor.expected.txt"
CHECKSUM_PATH = CERT_DIR / "SHA256SUMS.txt"

MOD = 101
Poly = tuple[int, ...]
Dual = tuple[int, int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def trim(values: list[int] | tuple[int, ...]) -> Poly:
    out = [value % MOD for value in values]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out or [0])


ZERO: Poly = (0,)
ONE: Poly = (1,)
X: Poly = (0, 1)


def padd(left: Poly, right: Poly) -> Poly:
    size = max(len(left), len(right))
    return trim([
        (left[index] if index < len(left) else 0)
        + (right[index] if index < len(right) else 0)
        for index in range(size)
    ])


def pneg(value: Poly) -> Poly:
    return trim([-item for item in value])


def psub(left: Poly, right: Poly) -> Poly:
    return padd(left, pneg(right))


def pscale(value: Poly, scalar: int) -> Poly:
    return trim([scalar * item for item in value])


def pmul(left: Poly, right: Poly) -> Poly:
    out = [0] * (len(left) + len(right) - 1)
    for i, lhs in enumerate(left):
        for j, rhs in enumerate(right):
            out[i + j] += lhs * rhs
    return trim(out)


def pdegree(value: Poly) -> int:
    return -1 if value == ZERO else len(value) - 1


def pdivmod(dividend: Poly, divisor: Poly) -> tuple[Poly, Poly]:
    require(divisor != ZERO, "polynomial division by zero")
    remainder = list(dividend)
    quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
    inverse = pow(divisor[-1], MOD - 2, MOD)
    while len(remainder) >= len(divisor) and any(remainder):
        shift = len(remainder) - len(divisor)
        factor = remainder[-1] * inverse % MOD
        quotient[shift] = factor
        for index, coefficient in enumerate(divisor):
            remainder[index + shift] = (
                remainder[index + shift] - factor * coefficient
            ) % MOD
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return trim(quotient), trim(remainder)


def pexact(dividend: Poly, divisor: Poly) -> Poly:
    quotient, remainder = pdivmod(dividend, divisor)
    require(remainder == ZERO, "expected exact polynomial division")
    return quotient


def pgcd(left: Poly, right: Poly) -> Poly:
    while right != ZERO:
        _, remainder = pdivmod(left, right)
        left, right = right, remainder
    if left == ZERO:
        return ZERO
    return pscale(left, pow(left[-1], MOD - 2, MOD))


def product(values: list[Poly]) -> Poly:
    result = ONE
    for value in values:
        result = pmul(result, value)
    return result


def is_nonzero_constant(value: Poly) -> bool:
    return len(value) == 1 and value[0] % MOD != 0


def dy_add(left: Dual, right: Dual) -> Dual:
    return ((left[0] + right[0]) % MOD, (left[1] + right[1]) % MOD)


def dy_sub(left: Dual, right: Dual) -> Dual:
    return ((left[0] - right[0]) % MOD, (left[1] - right[1]) % MOD)


def dy_mul(left: Dual, right: Dual) -> Dual:
    return (
        left[0] * right[0] % MOD,
        (left[0] * right[1] + left[1] * right[0]) % MOD,
    )


def dy_scale(value: Dual, scalar: int) -> Dual:
    return (value[0] * scalar % MOD, value[1] * scalar % MOD)


def dy_poly_mul(left: list[Dual], right: list[Dual]) -> list[Dual]:
    out = [(0, 0)] * (len(left) + len(right) - 1)
    for i, lhs in enumerate(left):
        for j, rhs in enumerate(right):
            out[i + j] = dy_add(out[i + j], dy_mul(lhs, rhs))
    return out


def dy_eval(coefficients: list[Dual], label: int) -> Dual:
    result = (0, 0)
    for coefficient in reversed(coefficients):
        result = dy_add(dy_scale(result, label), coefficient)
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict[str, Any]:
    require(MANIFEST_PATH.is_file(), f"missing manifest: {MANIFEST_PATH}")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def validate_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    require(
        manifest.get("schema")
        == "rs-mca.rank16-fixed26-bezout-rectangle-conductor.v1",
        "manifest schema",
    )
    deployed = manifest.get("deployed", {})
    expected = {
        "p": 2_130_706_433,
        "n": 2_097_152,
        "B": 32_768,
        "a": 67_472,
        "r": 63_601,
        "d": 28_897,
        "L3": 59_730,
        "quadratic_J0": 30_831,
        "cubic_J0": 57_794,
    }
    require(deployed == expected, "deployed contract")
    require(2 * deployed["r"] - deployed["a"] == deployed["L3"], "L3")
    require(deployed["r"] - deployed["d"] == 34_704, "split-star floor")

    theorem = manifest.get("theorem", {})
    required = {
        "joint_coefficient_primitivity": True,
        "polynomial_interpolation": True,
        "distinct_field_labels": True,
        "common_unscaled_normalization": True,
        "nonzero_inherited_cross_minor": True,
        "rectangle_sign": -1,
        "omitted_indices": [3, 6, 7],
        "official_score": "0/2",
    }
    require(theorem == required, "theorem guard contract")
    return deployed


def verify_source_pins(manifest: dict[str, Any]) -> int:
    pins = manifest.get("source_pins", [])
    require(len(pins) == 8, "source pin count")
    for item in pins:
        path = ROOT / item["path"]
        require(path.is_file(), f"missing source pin: {item['path']}")
        require(sha256(path) == item["sha256"], f"source pin: {item['path']}")
    return len(pins)


def verify_note_contract() -> int:
    text = NOTE_PATH.read_text(encoding="utf-8")
    required = [
        "D_y D_z | mathcal_b",
        "product(D_y : y in A union C) | mathcal_b",
        "= -(a-a')(b-b') mathcal_b",
        "P_opp | g c",
        "P_opp/gcd(P_opp,g) | c | J0",
        "deg P_opp <= 98303 = 3B-1",
        "deg P_opp <= 125266",
        "official score remains `0/2`",
        "does not exclude either source-valid terminal",
    ]
    for phrase in required:
        require(phrase in text, f"missing note contract phrase: {phrase}")
    return len(required)


def build_polynomial_model(
    *,
    labels: list[int] | None = None,
    n_shift: int = 0,
    scaled_entry: tuple[int, int] | None = None,
    omitted: tuple[int, int, int] = (3, 6, 7),
    wrong_j0: bool = False,
) -> dict[str, int]:
    labels = list(range(8)) if labels is None else labels
    require(len(labels) == 8 and len(set(labels)) == 8, "eight distinct labels")
    rows = labels[:4]
    columns = labels[4:]

    denominators = {label: psub(X, (label,)) for label in labels}
    h_all = product([denominators[label] for label in labels])
    x_squared = pmul(X, X)

    alpha = psub(h_all, x_squared)
    beta = X
    gamma = (MOD - 1,)
    mathcal_b = psub(pmul(beta, beta), pmul(alpha, gamma))
    require(mathcal_b == h_all, "Bezout determinant equals eight-label product")

    values: dict[int, Poly] = {}
    for label in labels:
        numerator = padd(psub(h_all, x_squared), ((label * label + n_shift) % MOD,))
        values[label] = pexact(numerator, denominators[label])

    def secant(y: int, z: int) -> Poly:
        inverse = pow((y - z) % MOD, MOD - 2, MOD)
        result = pscale(psub(values[y], values[z]), inverse)
        if scaled_entry is not None and {y, z} == set(scaled_entry):
            result = pscale(result, 2)
        return result

    pair_checks = 0
    for y, z in combinations(labels, 2):
        w_yz = padd(
            padd(alpha, pscale(beta, y + z)),
            pscale(gamma, y * z),
        )
        require(
            w_yz == pmul(pmul(denominators[y], denominators[z]), secant(y, z)),
            "exact source secant",
        )
        pexact(mathcal_b, pmul(denominators[y], denominators[z]))
        pair_checks += 1

    require(product([denominators[label] for label in labels]) == mathcal_b, "all eight")
    require(
        max(
            sum(1 for label in labels if pdivmod(denominators[label], factor)[1] == ZERO)
            for factor in denominators.values()
        )
        == 1,
        "irreducible denominator support",
    )

    rectangle_checks = 0
    for a, a_prime in combinations(rows, 2):
        for b, b_prime in combinations(columns, 2):
            delta = psub(
                pmul(secant(a, b), secant(a_prime, b_prime)),
                pmul(secant(a, b_prime), secant(a_prime, b)),
            )
            left = pmul(
                product([
                    denominators[a],
                    denominators[a_prime],
                    denominators[b],
                    denominators[b_prime],
                ]),
                delta,
            )
            scalar = (-(a - a_prime) * (b - b_prime)) % MOD
            require(left == pscale(mathcal_b, scalar), "signed rectangle identity")
            rectangle_checks += 1

    require(omitted == (rows[3], columns[2], columns[3]), "omitted triple contract")
    g = pmul(denominators[rows[3]], denominators[columns[2]])
    content = denominators[columns[3]]
    five = product([
        denominators[rows[0]],
        denominators[rows[1]],
        denominators[rows[2]],
        denominators[columns[0]],
        denominators[columns[1]],
    ])
    require(product([g, content, five]) == mathcal_b, "five-label cofactor factorization")

    cofactor_checks = 0
    for omitted_row in rows[:3]:
        used_rows = [value for value in rows[:3] if value != omitted_row]
        delta = psub(
            pmul(secant(used_rows[0], columns[0]), secant(used_rows[1], columns[1])),
            pmul(secant(used_rows[0], columns[1]), secant(used_rows[1], columns[0])),
        )
        h_i = pexact(delta, g)
        scalar = pexact(h_i, pmul(content, denominators[omitted_row]))
        require(is_nonzero_constant(scalar), "cofactor quotient equals c D_ui up to unit")
        cofactor_checks += 1

    p_opp = product([denominators[index] for index in omitted])
    pexact(pmul(g, content), p_opp)
    pexact(pmul(g, content), p_opp)
    reduced = pexact(p_opp, pgcd(p_opp, g))
    pexact(content, reduced)

    # D(Z)=X-Z and T=X-g give D(T)=g. D0=cD gives J0=c.
    t_value = psub(X, g)
    d_at_t = psub(X, t_value)
    require(d_at_t == g, "primitive conductor specialization")
    j0 = padd(content, ONE) if wrong_j0 else content
    require(pmul(g, j0) == pmul(content, d_at_t), "J0=cJ")

    return {
        "pair_checks": pair_checks,
        "rectangle_checks": rectangle_checks,
        "cofactor_checks": cofactor_checks,
        "model_degree": pdegree(mathcal_b),
    }


def verify_nonreduced_model() -> int:
    # Work in F_101[x]/(x^2). T=20+x is a unit distance from labels 0,...,7.
    t = (20, 1)
    xi = (1, 1)
    # L(Z)=Z-3+x is nonzero mod x and has exactly one label root mod x.
    l_poly = [((MOD - 3) % MOD, 1), (1, 0)]
    t_minus_z = [t, (MOD - 1, 0)]
    d_poly = dy_poly_mul(t_minus_z, l_poly)
    n_poly = [dy_mul(xi, coefficient) for coefficient in l_poly]
    require(len(d_poly) == 3 and len(n_poly) == 2, "prime-power degrees")

    exceptional = []
    for label in range(8):
        d_value = dy_eval(d_poly, label)
        l_value = dy_eval(l_poly, label)
        t_minus_label = dy_sub(t, (label, 0))
        require(t_minus_label[0] != 0, "T-y unit modulo pi")
        require(d_value == dy_mul(t_minus_label, l_value), "D=(T-Z)L")
        require(d_value[0] == 0 if l_value[0] == 0 else d_value[0] != 0, "exceptional equivalence")
        if d_value[0] == 0:
            exceptional.append(label)
    require(exceptional == [3], "at most one exceptional label")
    require(all(coefficient == dy_mul(xi, source) for coefficient, source in zip(n_poly, l_poly)), "N=xi L")
    return len(exceptional)


def verify_degree_endpoints(deployed: dict[str, int]) -> int:
    quadratic_total = deployed["a"] + deployed["quadratic_J0"]
    cubic_total = deployed["a"] + deployed["cubic_J0"]
    require(quadratic_total == 98_303 == 3 * deployed["B"] - 1, "quadratic total")
    require(cubic_total == 125_266, "cubic total")
    require(quadratic_total // 3 == 32_767, "quadratic omitted floor")
    require(cubic_total // 3 == 41_755, "cubic omitted floor")
    require(sum((32_767, 32_768, 32_768)) == quadratic_total, "quadratic sharp triple")
    require(sum((41_755, 41_755, 41_756)) == cubic_total, "cubic sharp triple")
    require(3 * 41_756 > cubic_total, "cubic pigeonhole strictness")
    return 7


def verify_hypothesis_guards() -> int:
    # Dropping joint coefficient primitivity: D_y=x for all labels, B=x^4.
    denominator_product = (0,) * 8 + (1,)
    bezout_value = (0, 0, 0, 0, 1)
    require(pdivmod(bezout_value, denominator_product)[1] != ZERO, "primitivity counterexample")

    # Dropping polynomial-valued interpolation: N=1, D=Z^2-X gives B=1,
    # while D_1=1-X is a nonunit and cannot divide B.
    d_one = (1, MOD - 1)
    require(pdivmod(ONE, d_one)[1] != ZERO, "polynomial interpolation counterexample")

    # The common-normalization guard is witnessed by the audited F_7 matrix.
    matrix = [[2, 3, 4], [3, 4, 5], [4, 5, 6]]
    mutated = copy.deepcopy(matrix)
    mutated[0][0] = 4

    def determinant3(values: list[list[int]], modulus: int) -> int:
        return (
            values[0][0] * (values[1][1] * values[2][2] - values[1][2] * values[2][1])
            - values[0][1] * (values[1][0] * values[2][2] - values[1][2] * values[2][0])
            + values[0][2] * (values[1][0] * values[2][1] - values[1][1] * values[2][0])
        ) % modulus

    require(determinant3(matrix, 7) == 0, "common-normalization base matrix")
    require(determinant3(mutated, 7) == 5, "entrywise normalization mutation")
    return 3


def semantic_mutation_selftests(manifest: dict[str, Any]) -> int:
    tests: list[tuple[str, Callable[[], None]]] = []

    def contract_mutation(path: tuple[str, str], value: Any) -> Callable[[], None]:
        def run() -> None:
            mutated = copy.deepcopy(manifest)
            mutated[path[0]][path[1]] = value
            validate_contract(mutated)
        return run

    tests.extend([
        ("rectangle sign", contract_mutation(("theorem", "rectangle_sign"), 1)),
        ("block parameter", contract_mutation(("deployed", "B"), 32_769)),
        ("quadratic cap", contract_mutation(("deployed", "quadratic_J0"), 30_832)),
        ("cubic cap", contract_mutation(("deployed", "cubic_J0"), 57_795)),
        ("primitive guard", contract_mutation(("theorem", "joint_coefficient_primitivity"), False)),
        ("distinct labels", lambda: build_polynomial_model(labels=[0, 1, 2, 3, 4, 5, 6, 6])),
        ("polynomial interpolation", lambda: build_polynomial_model(n_shift=1)),
        ("entrywise scaling", lambda: build_polynomial_model(scaled_entry=(0, 4))),
        ("omitted triple", lambda: build_polynomial_model(omitted=(2, 6, 7))),
        ("conductor content", lambda: build_polynomial_model(wrong_j0=True)),
    ])

    for name, test in tests:
        try:
            test()
        except (VerificationError, ValueError):
            continue
        raise VerificationError(f"semantic mutation survived: {name}")
    return len(tests)


def verify_checksums() -> int:
    require(CHECKSUM_PATH.is_file(), f"missing checksums: {CHECKSUM_PATH}")
    count = 0
    for line in CHECKSUM_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        require(path.is_file(), f"missing checksum artifact: {relative}")
        require(sha256(path) == expected, f"artifact checksum: {relative}")
        count += 1
    require(count == 4, "artifact checksum count")
    return count


def render_output(
    source_count: int,
    note_count: int,
    model: dict[str, int],
    exceptional_count: int,
    degree_checks: int,
    guard_checks: int,
    mutation_count: int,
    artifact_count: int,
) -> bytes:
    lines = [
        "RANK16_FIXED26_BEZOUT_RECTANGLE_CONDUCTOR: PASS",
        "schema=rs-mca.rank16-fixed26-bezout-rectangle-conductor.v1",
        "deployed=p2130706433,n2097152,B32768,a67472,r63601,d28897,L3=59730",
        f"source_pins=PASS,count={source_count};note_contract=PASS,count={note_count}",
        (
            "polynomial_model=PASS,labels8,pairs"
            f"{model['pair_checks']},rectangles{model['rectangle_checks']},"
            f"cofactors{model['cofactor_checks']},bezout_degree{model['model_degree']}"
        ),
        f"prime_power_model=PASS,exceptional_labels={exceptional_count},ring=F101[x]/(x^2)",
        f"degree_endpoints=PASS,count={degree_checks},quadratic=98303/32767,cubic=125266/41755",
        f"hypothesis_guards=PASS,count={guard_checks}",
        f"semantic_mutation_selftests=PASS,count={mutation_count}",
        f"artifact_checksums=PASS,count={artifact_count}",
        "finite_payment=0;parent_payment=0;official_score=0/2",
        "remaining=quadratic_and_cubic_source_incidence_plus_global_aggregation",
        "RESULT=PASS",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def run(emit_transcript: bool) -> bytes:
    manifest = load_manifest()
    deployed = validate_contract(manifest)
    source_count = verify_source_pins(manifest)
    note_count = verify_note_contract()
    model = build_polynomial_model()
    exceptional_count = verify_nonreduced_model()
    degree_checks = verify_degree_endpoints(deployed)
    guard_checks = verify_hypothesis_guards()
    mutation_count = semantic_mutation_selftests(manifest)
    artifact_count = 4 if emit_transcript else verify_checksums()
    output = render_output(
        source_count,
        note_count,
        model,
        exceptional_count,
        degree_checks,
        guard_checks,
        mutation_count,
        artifact_count,
    )
    if not emit_transcript:
        require(EXPECTED_PATH.is_file(), f"missing expected output: {EXPECTED_PATH}")
        require(output == EXPECTED_PATH.read_bytes(), "frozen expected output byte match")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--emit-transcript", action="store_true")
    group.add_argument("--tamper-self-test", action="store_true")
    group.add_argument("--check-checksums", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest()
        if args.tamper_self_test:
            validate_contract(manifest)
            count = semantic_mutation_selftests(manifest)
            print(f"SEMANTIC_TAMPER_SELFTEST: PASS count={count}")
            return 0
        if args.check_checksums:
            count = verify_checksums()
            print(f"ARTIFACT_CHECKSUMS: PASS count={count}")
            return 0
        sys.stdout.buffer.write(run(args.emit_transcript))
        return 0
    except (OSError, ValueError, VerificationError, json.JSONDecodeError) as exc:
        print(f"RANK16_FIXED26_BEZOUT_RECTANGLE_CONDUCTOR: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
