#!/usr/bin/env python3
"""Exact finite replay for the affine-line Steiner family's C1 ownership.

The mathematical statement is general over F_{p^m}. This verifier checks the
quadratic fixtures F_9/F_3 and F_25/F_5 used by the rs-mca deep-hole design
packet, plus two additional F_{p^2} controls. Bare invocation checks the
committed certificate.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "rs-mca-affine-steiner-quotient-owner-v1"
STATUS = "PROVED ALGEBRA / EXACT FINITE REPLAY"
DEFAULT_CERTIFICATE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "certificates"
    / "affine-steiner-quotient-owner"
    / "affine_steiner_quotient_owner.json"
)


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def is_prime(p: int) -> bool:
    if p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True


def legendre(a: int, p: int) -> int:
    if a % p == 0:
        return 0
    value = pow(a % p, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def least_nonsquare(p: int) -> int:
    for d in range(2, p):
        if legendre(d, p) == -1:
            return d
    raise VerificationError(f"no nonsquare found for p={p}")


@dataclass(frozen=True)
class QuadraticField:
    p: int
    nonsquare: int

    @classmethod
    def create(cls, p: int) -> "QuadraticField":
        require(is_prime(p) and p % 2 == 1, "p must be an odd prime")
        return cls(p=p, nonsquare=least_nonsquare(p))

    @property
    def q(self) -> int:
        return self.p * self.p

    def parts(self, x: int) -> tuple[int, int]:
        return x % self.p, (x // self.p) % self.p

    def encode(self, a: int, b: int) -> int:
        return (a % self.p) + self.p * (b % self.p)

    def add(self, x: int, y: int) -> int:
        a, b = self.parts(x)
        c, d = self.parts(y)
        return self.encode(a + c, b + d)

    def neg(self, x: int) -> int:
        a, b = self.parts(x)
        return self.encode(-a, -b)

    def sub(self, x: int, y: int) -> int:
        return self.add(x, self.neg(y))

    def mul(self, x: int, y: int) -> int:
        a, b = self.parts(x)
        c, d = self.parts(y)
        return self.encode(a * c + self.nonsquare * b * d, a * d + b * c)

    def pow(self, x: int, exponent: int) -> int:
        require(exponent >= 0, "negative exponent")
        result = 1
        base = x
        power = exponent
        while power:
            if power & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            power >>= 1
        return result

    def scalar(self, a: int) -> int:
        return self.encode(a, 0)

    def display(self, x: int) -> str:
        a, b = self.parts(x)
        return str(a) if b == 0 else f"{a}+{b}u"


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_mul(field: QuadraticField, left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = field.add(out[i + j], field.mul(a, b))
    return trim(out)


def locator(field: QuadraticField, roots: Iterable[int]) -> list[int]:
    out = [1]
    for root in roots:
        out = poly_mul(field, out, [field.neg(root), 1])
    return out


def linearized(field: QuadraticField, gamma: int, x: int) -> int:
    return field.sub(field.pow(x, field.p), field.mul(gamma, x))


def canonical_payload(value: dict[str, Any]) -> bytes:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return json.dumps(
        unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def payload_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_payload(value)).hexdigest()


def read_certificate(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"cannot read certificate {path}: {exc}") from exc
    require(isinstance(value, dict), "certificate root must be an object")
    return value


def verify_certificate(candidate: dict[str, Any], payload: dict[str, Any]) -> None:
    require(
        candidate.get("payload_sha256") == payload_sha256(candidate),
        "certificate payload hash mismatch",
    )
    require(candidate == payload, "certificate mismatch")


def check_prime(p: int) -> dict[str, Any]:
    field = QuadraticField.create(p)
    q = field.q
    all_elements = list(range(q))
    nonzero = list(range(1, q))

    gamma_to_directions: dict[int, set[frozenset[int]]] = {}
    for v in nonzero:
        gamma = field.pow(v, p - 1)
        direction = frozenset(field.mul(field.scalar(a), v) for a in range(p))
        gamma_to_directions.setdefault(gamma, set()).add(direction)

    require(
        len(gamma_to_directions) == (q - 1) // (p - 1),
        "direction/gamma count",
    )
    require(
        all(len(tags) == 1 for tags in gamma_to_directions.values()),
        "gamma determines direction",
    )

    all_lines: set[tuple[int, ...]] = set()
    slope_multiplicities: dict[int, int] = {}
    checks = 3

    for gamma in sorted(gamma_to_directions):
        kernel = {
            x for x in all_elements if linearized(field, gamma, x) == 0
        }
        require(len(kernel) == p, "kernel size")
        checks += 1
        v = next(x for x in kernel if x != 0)
        expected_kernel = {
            field.mul(field.scalar(a), v) for a in range(p)
        }
        require(kernel == expected_kernel, "kernel is one F_p direction")
        checks += 1

        fibers: dict[int, set[int]] = {}
        for x in all_elements:
            fibers.setdefault(linearized(field, gamma, x), set()).add(x)
        require(len(fibers) == q // p, "image size")
        require(all(len(fiber) == p for fiber in fibers.values()), "uniform fibers")
        checks += 2

        for z, fiber in fibers.items():
            a0 = next(iter(fiber))
            expected = {field.add(a0, k) for k in kernel}
            require(fiber == expected, "fiber is affine F_p-line")

            coeffs = locator(field, sorted(fiber))
            target = [field.neg(z)] + [0] * (p - 1) + [1]
            target[1] = field.neg(gamma)
            require(coeffs == target, "fiber locator is X^p-gamma X-z")

            # The received-line word -x^p + gamma*x + z vanishes exactly here.
            zeros = {
                x
                for x in all_elements
                if field.add(
                    field.neg(field.pow(x, p)),
                    field.add(field.mul(gamma, x), z),
                )
                == 0
            }
            require(zeros == fiber, "received-line zero set")

            line_key = tuple(sorted(fiber))
            require(
                line_key not in all_lines,
                "affine line has unique quotient profile",
            )
            all_lines.add(line_key)
            checks += 4

        slope_multiplicities[gamma] = len(fibers)

    expected_lines = q * (q - 1) // (p * (p - 1))
    require(len(all_lines) == expected_lines, "Steiner affine-line count")
    require(
        set(slope_multiplicities.values()) == {q // p},
        "constant witnesses per slope",
    )
    checks += 2

    # Every pair of distinct points lies in exactly one line.
    pair_counts: dict[tuple[int, int], int] = {}
    for line in all_lines:
        for i, x in enumerate(line):
            for y in line[i + 1 :]:
                pair_counts[(x, y)] = pair_counts.get((x, y), 0) + 1
    require(len(pair_counts) == q * (q - 1) // 2, "all point pairs covered")
    require(set(pair_counts.values()) == {1}, "Steiner S(2,p,q) uniqueness")
    checks += 2

    return {
        "p": p,
        "q": q,
        "quadratic_nonsquare": field.nonsquare,
        "quotient_profiles": len(gamma_to_directions),
        "fibers_per_profile": q // p,
        "total_affine_lines": len(all_lines),
        "expected_affine_lines": expected_lines,
        "checks": checks,
        "verdict": "C1_QUOTIENT_OWNED",
    }


def build_payload() -> dict[str, Any]:
    rows = [check_prime(p) for p in (3, 5, 7, 11)]
    require(
        rows[0]["quotient_profiles"] == 4
        and rows[0]["total_affine_lines"] == 12,
        "F9 fixture",
    )
    require(
        rows[1]["quotient_profiles"] == 6
        and rows[1]["total_affine_lines"] == 30,
        "F25 fixture",
    )
    total_checks = sum(row["checks"] for row in rows) + 2
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "claim": (
            "For each direction gamma=v^(p-1), x -> x^p-gamma*x is an F_p-linear "
            "quotient with kernel F_p v; its fibers are exactly the affine F_p-lines "
            "and have locator X^p-gamma X-z. Hence the sharp affine-line Steiner "
            "family is C1 quotient-owned, not primitive."
        ),
        "rows": rows,
        "total_checks": total_checks,
    }
    payload["payload_sha256"] = payload_sha256(payload)
    return payload


def run_tamper_selftest(payload: dict[str, Any]) -> None:
    mutations = (
        ("claim", lambda x: x.__setitem__("claim", x["claim"] + " tampered")),
        ("hash", lambda x: x.__setitem__("payload_sha256", "0" * 64)),
        (
            "row-count",
            lambda x: x["rows"][0].__setitem__("total_affine_lines", 11),
        ),
        (
            "slope-count",
            lambda x: x["rows"][1].__setitem__("quotient_profiles", 7),
        ),
        ("status", lambda x: x.__setitem__("status", "PROVED")),
        ("checks", lambda x: x.__setitem__("total_checks", x["total_checks"] + 1)),
    )
    caught = 0
    for label, mutate in mutations:
        bad = copy.deepcopy(payload)
        mutate(bad)
        try:
            verify_certificate(bad, payload)
        except VerificationError:
            caught += 1
        else:
            raise VerificationError(f"tamper not caught: {label}")

    rehashed = copy.deepcopy(payload)
    rehashed["claim"] += " tampered and rehashed"
    rehashed["payload_sha256"] = payload_sha256(rehashed)
    try:
        verify_certificate(rehashed, payload)
    except VerificationError:
        caught += 1
    else:
        raise VerificationError("tamper not caught: rehashed-claim")

    total = len(mutations) + 1
    require(caught == total, "tamper rejection count")
    print(f"TAMPER_SELFTEST: PASS ({caught}/{total})")


def main() -> int:
    parser = argparse.ArgumentParser()
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--write", type=Path)
    output.add_argument("--check", type=Path)
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    require(payload["payload_sha256"] == payload_sha256(payload), "payload hash")

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        certificate_path = args.check or DEFAULT_CERTIFICATE
        verify_certificate(read_certificate(certificate_path), payload)

    if args.tamper_selftest:
        run_tamper_selftest(payload)

    print(f"RESULT: PASS ({payload['total_checks']}/{payload['total_checks']})")
    print("STATUS: PROVED / C1 QUOTIENT-OWNED")
    print(f"PAYLOAD_SHA256: {payload['payload_sha256']}")
    for row in payload["rows"]:
        print(
            f"F_{row['q']}/F_{row['p']}: "
            f"{row['quotient_profiles']} quotient maps x "
            f"{row['fibers_per_profile']} fibers = "
            f"{row['total_affine_lines']} affine lines"
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"RESULT: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
