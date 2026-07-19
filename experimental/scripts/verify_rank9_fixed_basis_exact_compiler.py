#!/usr/bin/env python3
"""Verify the pinned rank-nine fixed-basis exact compiler formalization."""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
SOURCE_REL = (
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_fixed_basis_fibre_route_cut_v1.md"
)
SOURCE_PATH = ROOT / SOURCE_REL
LEAN_PATH = (
    ROOT
    / "experimental/lean/rank9_fixed_basis_exact_compiler/"
    / "Rank9FixedBasisExactCompiler.lean"
)
README_PATH = ROOT / "experimental/lean/rank9_fixed_basis_exact_compiler/README.md"
EXPECTED_SOURCE_SHA256 = (
    "066ebeff9e738a1462ad351edada78c47b4b5a53f926929d98eecb12dee42528"
)
EXPECTED_LEAN_SHA256 = (
    "e2b6286e917e33f97a1a28f076b9c2ca62aa30c99780947c86ea5d1cbb932d65"
)


def normalized(text: str) -> str:
    return " ".join(text.split())


def declaration_block(source: str, marker: str) -> str:
    start_marker = f"\n{marker}"
    start = source.index(start_marker) + 1
    end = source.find("\n\n", start)
    if end < 0:
        raise ValueError(f"unterminated declaration: {marker}")
    return source[start:end]


def theorem_block(source: str, name: str) -> str:
    marker = f"\ntheorem {name}"
    start = source.index(marker) + 1
    ends = [
        pos
        for pos in (
            source.find("\n\n/--", start),
            source.find("\n\n#print", start),
            source.find("\n\nend ", start),
        )
        if pos >= 0
    ]
    if not ends:
        raise ValueError(f"unterminated theorem: {name}")
    return source[start : min(ends)]


def theorem_statement(source: str, name: str) -> str:
    block = theorem_block(source, name)
    statement, separator, _proof = block.partition(":= by")
    if not separator:
        raise ValueError(f"missing proof boundary: {name}")
    return normalized(statement)


def valid_docstring(source: str, name: str, labels: tuple[str, ...]) -> bool:
    marker = f"\ntheorem {name}"
    try:
        theorem_start = source.index(marker)
        doc_start = source.rindex("/--", 0, theorem_start)
        doc_end = source.index("-/", doc_start, theorem_start)
    except ValueError:
        return False
    doc = source[doc_start : doc_end + 2]
    return (
        SOURCE_REL in doc
        and "`3404d21`" in doc
        and all(label in doc for label in labels)
    )


EXPECTED_DEFINITIONS: dict[str, str] = {
    "def factorial": normalized(
        """def factorial : Nat → Nat
        | 0 => 1
        | k + 1 => (k + 1) * factorial k"""
    ),
    "def descFactorial": normalized(
        """def descFactorial (m : Nat) : Nat → Nat
        | 0 => 1
        | k + 1 => (m - k) * descFactorial m k"""
    ),
    "def binom": normalized(
        "def binom (m k : Nat) : Nat := descFactorial m k / factorial k"
    ),
    "abbrev n": normalized(
        """abbrev n : Nat := 2097152
        abbrev j : Nat := 981104
        abbrev lowBase : Nat := 67480
        abbrev target : Nat := 17907572507584
        abbrev m20 : Nat := (21 * j) / 20 + 1
        abbrev c0 : Nat := binom lowBase 8
        abbrev eMax : Nat := (target + 1) * c0 - 20 * binom n 8 - 1"""
    ),
    "def total": normalized(
        """def total : List Nat → Nat
        | [] => 0
        | m :: ms => m + total ms"""
    ),
    "def excess20": normalized(
        """def excess20 : List Nat → Nat
        | [] => 0
        | m :: ms => (m - 20) + excess20 ms"""
    ),
}


EXPECTED_STATEMENTS: dict[str, str] = {
    "c0_value": normalized(
        "theorem c0_value : c0 = 10658592438443717273371372062592575"
    ),
    "large_union_threshold_iff": normalized(
        """theorem large_union_threshold_iff (MB : Nat) :
        21 * (MB - j) > MB ↔ m20 ≤ MB"""
    ),
    "low_union_interval_iff": normalized(
        """theorem low_union_interval_iff (MB : Nat) :
        (j < MB ∧ MB < m20) ↔ (981105 ≤ MB ∧ MB ≤ 1030159)"""
    ),
    "cap20_tail_value": normalized(
        "theorem cap20_tail_value : (20 * binom n 8) / c0 = 17411776716968"
    ),
    "cap20_margin_value": normalized(
        """theorem cap20_margin_value :
        target - (20 * binom n 8) / c0 = 495795790616"""
    ),
    "cap21_tail_and_excess": normalized(
        """theorem cap21_tail_and_excess :
        (21 * binom n 8) / c0 = 18282365552816 ∧
        (21 * binom n 8) / c0 - target = 374793045232"""
    ),
    "aggregate_excess_max_value": normalized(
        """theorem aggregate_excess_max_value :
        eMax = 5284485264881189380664190436821715347228277374"""
    ),
    "aggregate_excess_sharp": normalized(
        """theorem aggregate_excess_sharp :
        (20 * binom n 8 + eMax) / c0 = target ∧
        (20 * binom n 8 + (eMax + 1)) / c0 = target + 1"""
    ),
    "total_le_twenty_mul_length": normalized(
        """theorem total_le_twenty_mul_length
        (counts : List Nat)
        (hCap : ∀ m ∈ counts, m ≤ 20) :
        total counts ≤ 20 * counts.length"""
    ),
    "total_le_baseline_add_excess": normalized(
        """theorem total_le_baseline_add_excess (counts : List Nat) :
        total counts ≤ 20 * counts.length + excess20 counts"""
    ),
    "uniform_cap20_compiler": normalized(
        """theorem uniform_cap20_compiler
        (H : Nat)
        (counts : List Nat)
        (hLower : H * c0 ≤ total counts)
        (hCard : counts.length ≤ binom n 8)
        (hCap : ∀ m ∈ counts, m ≤ 20) :
        H ≤ 17411776716968"""
    ),
    "aggregate_excess_compiler": normalized(
        """theorem aggregate_excess_compiler
        (H : Nat)
        (counts : List Nat)
        (hLower : H * c0 ≤ total counts)
        (hCard : counts.length ≤ binom n 8)
        (hExcess : excess20 counts ≤ eMax) :
        H ≤ target"""
    ),
}


DOCSTRING_LABELS: dict[str, tuple[str, ...]] = {
    "c0_value": ("(1.4)",),
    "large_union_threshold_iff": ("(3.1)",),
    "low_union_interval_iff": ("(3.2)",),
    "cap20_tail_value": ("(4.1)",),
    "cap20_margin_value": ("(4.2)",),
    "cap21_tail_and_excess": ("(4.3)",),
    "aggregate_excess_max_value": ("(4.5)",),
    "aggregate_excess_sharp": ("(4.5)",),
    "total_le_twenty_mul_length": ("(4.1)",),
    "total_le_baseline_add_excess": ("(4.4)", "(4.5)"),
    "uniform_cap20_compiler": ("(1.6)", "(4.1)"),
    "aggregate_excess_compiler": ("(1.6)", "(4.4)", "(4.5)"),
}


FORBIDDEN_LEAN = re.compile(
    r"\b(?:sorry|admit|axiom|constant|opaque|sorryAx|variable|include|omit|"
    r"native_decide|Lean\.ofReduceBool|trustCompiler)\b"
)


def definitions_valid(lean: str) -> bool:
    try:
        return all(
            normalized(declaration_block(lean, marker)) == expected
            for marker, expected in EXPECTED_DEFINITIONS.items()
        )
    except ValueError:
        return False


def theorem_statements_valid(lean: str) -> bool:
    try:
        return all(
            theorem_statement(lean, name) == expected
            for name, expected in EXPECTED_STATEMENTS.items()
        )
    except ValueError:
        return False


def theorem_docstrings_valid(lean: str) -> bool:
    return all(
        valid_docstring(lean, name, DOCSTRING_LABELS[name])
        for name in EXPECTED_STATEMENTS
    )


def theorem_name_set_valid(lean: str) -> bool:
    names = set(re.findall(r"(?m)^theorem ([A-Za-z0-9_]+)", lean))
    return names == set(EXPECTED_STATEMENTS)


def valid_lean_file(lean: str) -> bool:
    return (
        hashlib.sha256(lean.encode()).hexdigest() == EXPECTED_LEAN_SHA256
        and FORBIDDEN_LEAN.search(lean) is None
        and definitions_valid(lean)
        and theorem_name_set_valid(lean)
        and theorem_statements_valid(lean)
        and theorem_docstrings_valid(lean)
    )


def source_binom(m: int, k: int) -> int:
    descending = math.prod(m - i for i in range(k))
    return descending // math.factorial(k)


def verify(check_only: bool) -> tuple[int, int]:
    passed = 0
    total_checks = 0

    def check(condition: bool, label: str) -> None:
        nonlocal passed, total_checks
        total_checks += 1
        if condition:
            passed += 1
        elif not check_only:
            print(f"FAIL: {label}")

    source_bytes = SOURCE_PATH.read_bytes()
    source = source_bytes.decode()
    lean = LEAN_PATH.read_text()
    readme = README_PATH.read_text()

    check(
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
        "source blob pinned to integrated 3404d21 authority",
    )
    for heading in (
        "## 1. Frozen deployed interface",
        "## 3. Exact trichotomy and the corrected integer threshold",
        "## 4. Exact deployed compiler",
        "## 5. Exact counterexample to the pointwise cap",
    ):
        check(heading in source, f"source heading: {heading}")
    for label in ("1.4", "1.6", "3.1", "3.2", "4.1", "4.2", "4.3", "4.4", "4.5"):
        check(f"\\tag{{{label}}}" in source, f"source equation label: {label}")
    check("`3404d21`" in readme, "README source pin")
    check("## Theorem map" in readme, "README theorem map")
    check("Eq. (5.4), five-pencil realization" in readme, "README nonformalized boundary")

    check(
        hashlib.sha256(lean.encode()).hexdigest() == EXPECTED_LEAN_SHA256,
        "Lean blob pinned to exact reviewed declarations and proofs",
    )
    check(FORBIDDEN_LEAN.search(lean) is None, "Lean forbidden declaration tokens")
    check(theorem_name_set_valid(lean), "Lean exact theorem-name set")
    for marker, expected in EXPECTED_DEFINITIONS.items():
        try:
            actual = normalized(declaration_block(lean, marker))
        except ValueError:
            actual = ""
        check(actual == expected, f"Lean exact definition: {marker}")
    for name, expected in EXPECTED_STATEMENTS.items():
        try:
            actual = theorem_statement(lean, name)
        except ValueError:
            actual = ""
        check(actual == expected, f"Lean exact theorem statement: {name}")
        check(
            valid_docstring(lean, name, DOCSTRING_LABELS[name]),
            f"Lean source-pinned docstring: {name}",
        )

    n = 2_097_152
    j = 981_104
    low_base = 67_480
    target = 17_907_572_507_584
    c0 = source_binom(low_base, 8)
    n8 = source_binom(n, 8)
    m20 = (21 * j) // 20 + 1
    cap20 = (20 * n8) // c0
    cap21 = (21 * n8) // c0
    emax = (target + 1) * c0 - 20 * n8 - 1

    arithmetic_checks = (
        (c0 == math.comb(low_base, 8), "source binomial C(67480,8)"),
        (n8 == math.comb(n, 8), "source binomial C(n,8)"),
        (c0 == 10_658_592_438_443_717_273_371_372_062_592_575, "C0"),
        (m20 == 1_030_160, "sharp union threshold"),
        (21 * (m20 - j) == 1_030_176, "upper adjacent product"),
        (21 * (m20 - j) > m20, "upper adjacent strict side"),
        (21 * ((m20 - 1) - j) == 1_030_155, "lower adjacent product"),
        (21 * ((m20 - 1) - j) < m20 - 1, "lower adjacent strict side"),
        (cap20 == 17_411_776_716_968, "cap-20 quotient"),
        (target - cap20 == 495_795_790_616, "cap-20 target margin"),
        (cap21 == 18_282_365_552_816, "cap-21 quotient"),
        (cap21 - target == 374_793_045_232, "cap-21 target excess"),
        (
            emax
            == 5_284_485_264_881_189_380_664_190_436_821_715_347_228_277_374,
            "aggregate excess maximum",
        ),
        (20 * n8 + emax == (target + 1) * c0 - 1, "last safe numerator"),
        ((20 * n8 + emax) // c0 == target, "last safe quotient"),
        ((20 * n8 + emax + 1) // c0 == target + 1, "first unsafe quotient"),
    )
    for condition, label in arithmetic_checks:
        check(condition, label)

    for candidate in range(m20 - 3, m20 + 4):
        expected = candidate >= m20
        excludes_21 = 21 * (candidate - j) > candidate
        check(excludes_21 == expected, f"threshold equivalence M={candidate}")

    if not check_only:
        print("RANK-NINE FIXED-BASIS EXACT COMPILER VERIFIER")
        print("source: integrated note at 3404d21; exact Python integers")
        print("Lean declarations: 12 exact statements; 6 exact definition blocks")
    return passed, total_checks


def tamper_selftest() -> None:
    lean = LEAN_PATH.read_text()
    false_shadow = """theorem cap20_tail_value : True := by
  exact True.intro
-- (20 * binom n 8) / c0 = 17411776716968 := by
--   decide"""
    original_cap20 = """theorem cap20_tail_value :
    (20 * binom n 8) / c0 = 17411776716968 := by
  decide"""
    commented_shadow = f"""/-
{original_cap20}
-/
{false_shadow}"""
    constant_escape = lean.replace(
        "namespace Rank9FixedBasisExactCompiler",
        "namespace Rank9FixedBasisExactCompiler\n\nconstant auditBogus : False",
        1,
    ).replace(
        "theorem c0_value :\n    c0 = 10658592438443717273371372062592575 := by\n  decide",
        "theorem c0_value :\n    c0 = 10658592438443717273371372062592575 := by\n  exact False.elim auditBogus",
        1,
    )
    variable_escape = lean.replace(
        "namespace Rank9FixedBasisExactCompiler",
        "namespace Rank9FixedBasisExactCompiler\n\nvariable (hBogus : False)\ninclude hBogus",
        1,
    ).replace(
        "theorem c0_value :\n    c0 = 10658592438443717273371372062592575 := by\n  decide",
        "theorem c0_value :\n    c0 = 10658592438443717273371372062592575 := by\n  exact False.elim hBogus",
        1,
    )
    mutations = (
        lean.replace("17411776716968", "17411776716969", 1),
        lean.replace("\ntheorem aggregate_excess_compiler", "\n-- theorem aggregate_excess_compiler", 1),
        lean.replace("    H ≤ 17411776716968 := by", "    H ≤ 17411776716968 := by\n  sorry", 1),
        lean.replace("(hExcess : excess20 counts ≤ eMax)", "(hExcess : excess20 counts < eMax)", 1),
        lean.replace(original_cap20, false_shadow, 1),
        lean.replace("    (hLower : H * c0 ≤ total counts)", "    (hBogus : False)\n    (hLower : H * c0 ≤ total counts)", 1),
        lean.replace("namespace Rank9FixedBasisExactCompiler", "namespace Rank9FixedBasisExactCompiler\n\naxiom auditBogus : False", 1),
        lean.replace(
            "abbrev eMax : Nat := (target + 1) * c0 - 20 * binom n 8 - 1",
            "abbrev eMax : Nat := 5284485264881189380664190436821715347228277374",
            1,
        ),
        lean.replace("  decide", "  native_decide", 1),
        lean.replace(original_cap20, commented_shadow, 1),
        constant_escape,
        variable_escape,
    )
    caught = sum(not valid_lean_file(mutated) for mutated in mutations)
    if caught != len(mutations):
        raise AssertionError(f"tamper-selftest caught {caught}/{len(mutations)}")
    print(f"tamper-selftest: caught {caught}/{len(mutations)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="print only the result")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        tamper_selftest()
    passed, total_checks = verify(args.check)
    if passed != total_checks:
        print(f"RESULT: FAIL ({passed}/{total_checks})")
        return 1
    print(f"RESULT: PASS ({passed}/{total_checks})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
