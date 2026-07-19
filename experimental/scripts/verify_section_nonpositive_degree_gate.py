#!/usr/bin/env python3
"""Verify the universal section-nonpositive degree gate and correspondence."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
LEAN_PATH = (
    ROOT
    / "experimental/lean/section_nonpositive_extraction/"
    / "SectionNonpositiveExtraction.lean"
)


def normalized(text: str) -> str:
    return " ".join(text.split())


def valid_degree_gate(source: str) -> bool:
    marker = "\ntheorem degree_gate\n"
    try:
        start = source.index(marker) + 1
        end = source.index("\n\n/-- #721 §4.1 degree gate, boolean form", start)
    except ValueError:
        return False
    block = source[start:end]
    statement = normalized(
        """theorem degree_gate
        (n k a : Nat)
        (hk : 1 ≤ k)
        (hkn : k < n)
        (_hka : k + 1 ≤ a)
        (_ha : a ≤ n)
        (hJ : SectionNonpositive n k a) :
        2 * a - k ≤ n - 1 := by"""
    )
    forbidden = re.search(r"\b(?:sorry|admit|axiom|opaque|sorryAx)\b", block)
    return statement in normalized(block) and forbidden is None


def verify(check_only: bool) -> tuple[int, int]:
    passed = 0
    total = 0

    def check(condition: bool, label: str) -> None:
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
        elif not check_only:
            print(f"FAIL: {label}")

    canonical = (
        ROOT
        / "experimental/notes/thresholds/"
        / "canonical_reduced_rational_host_compiler.md"
    ).read_text()
    consumer = (
        ROOT
        / "experimental/notes/thresholds/"
        / "section_nonpositive_extraction_counterexample.md"
    ).read_text()
    lean = LEAN_PATH.read_text()
    readme = (
        ROOT / "experimental/lean/section_nonpositive_extraction/README.md"
    ).read_text()

    check("### 4.1 The section-nonpositive degree gate" in canonical, "source label")
    check("From `a^2 <= n(k-1)`" in canonical, "source hypothesis")
    check("`2a-k <= n-1`" in canonical, "source conclusion")
    check(
        "the section-nonpositive gate forces `2a - k <= n-1`" in consumer,
        "counterexample consumer",
    )
    check("theorem degree_gate_n_le_40" in lean, "finite API retained")
    check(valid_degree_gate(lean), "anchored universal Lean declaration")
    check(
        "Polynomial/interpolation semantics and rational-host extraction | none"
        in readme,
        "theorem map nonclaim",
    )

    applicable = 0
    for n in range(129):
        for k in range(n):
            for a in range(n + 1):
                if 1 <= k and k + 1 <= a <= n and a * a <= n * (k - 1):
                    applicable += 1
                    check(2 * a - k <= n - 1, f"degree gate n={n},k={k},a={a}")

    check(applicable > 0, "nonvacuous exhaustive range")
    for n, k, a in ((8, 3, 4), (9, 2, 3), (16, 2, 4), (40, 10, 17)):
        check(
            a * a <= n * (k - 1) and 2 * a - k <= n - 1,
            f"named boundary n={n},k={k},a={a}",
        )

    if not check_only:
        print("SECTION-NONPOSITIVE DEGREE-GATE SOURCE VERIFIER")
        print(f"range: 0 <= n <= 128; applicable rows: {applicable}")
        print("source: compiler section 4.1; Lean declaration: degree_gate")
    return passed, total


def tamper_selftest() -> None:
    lean = LEAN_PATH.read_text()
    caught = 0
    caught += int(
        not valid_degree_gate(lean.replace("2 * a - k ≤ n - 1", "2 * a - k ≤ n - 2", 1))
    )
    caught += int(
        not valid_degree_gate(lean.replace("\ntheorem degree_gate\n", "\n-- theorem degree_gate\n", 1))
    )
    caught += int(
        not valid_degree_gate(lean.replace("2 * a - k ≤ n - 1 := by", "2 * a - k ≤ n - 1 := by\n  sorry", 1))
    )
    caught += int(
        not valid_degree_gate(
            lean.replace(
                "    (hkn : k < n)\n    (_hka : k + 1 ≤ a)",
                "    (hkn : k ≤ n)\n    (_hka : k + 1 ≤ a)",
                1,
            )
        )
    )
    if caught != 4:
        raise AssertionError(f"tamper-selftest caught {caught}/4")
    print("tamper-selftest: caught 4/4")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="print only the result")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        tamper_selftest()
    passed, total = verify(args.check)
    if passed != total:
        print(f"RESULT: FAIL ({passed}/{total})")
        return 1
    print(f"RESULT: PASS ({passed}/{total})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
