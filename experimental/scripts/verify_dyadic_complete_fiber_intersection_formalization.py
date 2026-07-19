#!/usr/bin/env python3
"""Fail-closed source/proof checks for complete-fiber intersection in Lean."""

from __future__ import annotations

import argparse
import copy
import hashlib
import re
import sys
from pathlib import Path
from typing import Callable, Dict, Sequence


class VerificationError(RuntimeError):
    """A source, statement, package, proof-boundary, or tamper check failed."""


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "experimental/lean/dyadic_complete_fiber_slicing"
PATHS = {
    "source": ROOT / "experimental/notes/l2/dyadic_complete_fiber_slicing_route_cut.md",
    "lean": PACKAGE / "DyadicCompleteFiberSlicingTarget.lean",
    "audit": ROOT / "experimental/notes/l2/dyadic_complete_fiber_intersection_formalization.md",
    "readme": PACKAGE / "README.md",
    "lakefile": PACKAGE / "lakefile.toml",
    "manifest": PACKAGE / "lake-manifest.json",
    "toolchain": PACKAGE / "lean-toolchain",
    "gitignore": PACKAGE / ".gitignore",
}
EXPECTED_SHA256 = {
    "source": "fba4b3541f6f6c982ae9327fcdcf14b11ba266e6ce09647f0b95d30b70369e13",
    "lean": "35942729e65815a01e79aacdece585598d57ccf249786d19c6562d59ae46adb8",
    "audit": "b298de8eeb7b64e146d445b2edf76a8c75cee2ce9b53d20b54515198e14d038a",
    "readme": "e5d5364a86cad48d780fdba8208eb08ed3ec9477bc453d37e98d0c77911889d3",
    "lakefile": "c79d6e98ca0f4b2fbd2838eb1e4fb62737494bf40725e519107a2282d0fa1dbf",
    "manifest": "fb51ea78ca173a86327d64cf4219c8ff3baeb43170416d4898ec41e694857a23",
    "toolchain": "db7bb24b756d745bbde83fe92718b51bd3625dae3701ba0f598d0eedcd3f3028",
    "gitignore": "5375c2c5e323f40c0031aa8c82f66bb9197214001039e6a8c9ff2a5eb3aa24a9",
}

MAIN_SIGNATURE = """theorem completeFiberIntersection
    (H : Subgroup Fˣ) [Fintype H] [LinearOrder H]
    (n K m c : Nat)
    (hcard : Fintype.card H = n)
    (hrange : 1 ≤ K ∧ K ≤ m ∧ m ≤ n)
    (hc : c ∣ n)
    (U : H → F)
    (P Q : Polynomial F)
    (hP : inReceivedList H K m U P)
    (hQ : inReceivedList H K m U Q)
    (hne : P ≠ Q) :
    ((completeFiberSet H c (canonicalSupport H m U P)) ∩
      completeFiberSet H c (canonicalSupport H m U Q)).card ≤
      (K - 1) / c := by"""

SOURCE_ANCHORS = (
    "Status: PROVED theorem and finite ROUTE_CUT; the official score remains `0/2`.",
    "For every two distinct\n`P,Q in L(U)`,",
    "|E_c(P) intersect E_c(Q)| <= h_c.                       (1)",
    "Every `pi_c`-fiber has exactly `c` elements.",
    "The quantifier over `U` is universal.",
    "The standalone Lean 4.28 / Mathlib package at",
    "`DyadicCompleteFiberSlicing.completeFiberIntersection`",
    "does not add a public theorem parameter",
    "does not certify the packing consequences (2)--(3)",
    "the residual `1792`-profile cap",
    "Grand List, Grand MCA, or an exact-threshold conclusion",
)

PROOF_ANCHORS = (
    "noncomputable section",
    "local instance : DecidableEq F := Classical.decEq F",
    "private theorem canonicalSupport_subset_agreementSet",
    "private theorem powerFiber_card",
    "IsCyclic.card_powMonoidHom_ker H c",
    "MonoidHom.card_fiber_eq_of_mem_range f",
    "Finset.sum_card_fiberwise_eq_card_filter",
    "have hfieldPointsRoots : fieldPoints.val ⊆ (P - Q).roots",
    "Polynomial.card_le_degree_of_subset_roots",
    "Polynomial.natDegree_sub_le P Q",
    "have hcpos : 0 < c",
    "Nat.le_div_iff_mul_le hcpos",
)

AUDIT_ANCHORS = (
    "## Status\n\nPROVED",
    "`DyadicCompleteFiberSlicing.completeFiberIntersection`",
    "no `DecidableEq F` binder is exported",
    "`IsCyclic.card_powMonoidHom_ker`",
    "`Finset.sum_card_fiberwise_eq_card_filter`",
    "`P(x)=U(x)=Q(x)`",
    "`Nat.le_div_iff_mul_le`",
    "[propext, Classical.choice, Quot.sound]",
    "There is no `sorry`, `admit`, `sorryAx`, custom `axiom`, or custom `opaque`",
    "certifies source equation (1) only",
    "unproved uniform residual cap",
    "Grand\nList, Grand MCA",
    "not\nused anywhere in this theorem",
)

README_ANCHORS = (
    "# Dyadic complete-fiber slicing formalization map",
    "`DyadicCompleteFiberSlicing.completeFiberIntersection` | PROVED",
    "The file's local classical `DecidableEq F` is an elaboration instance",
    "[propext, Classical.choice, Quot.sound]",
    "verify_role07_dyadic_full_fiber_cut.py",
    "The arithmetic replay does not verify the\nfield-theoretic proof",
    "This package certifies equation (1) only",
    "the residual\n`1792`-profile cap",
)


def read_bundle() -> Dict[str, str]:
    bundle: Dict[str, str] = {}
    for key, path in PATHS.items():
        try:
            bundle[key] = path.read_text(encoding="utf-8")
        except OSError as error:
            raise VerificationError(
                f"cannot read {path.relative_to(ROOT)}: {error}"
            ) from error
    return bundle


def verify_bundle(bundle: Dict[str, str]) -> int:
    checks = 0

    def require(condition: bool, message: str) -> None:
        nonlocal checks
        if not condition:
            raise VerificationError(message)
        checks += 1

    for key, expected in EXPECTED_SHA256.items():
        actual = hashlib.sha256(bundle[key].encode("utf-8")).hexdigest()
        require(actual == expected, f"pinned {key} artifact changed")

    source = bundle["source"]
    lean = bundle["lean"]
    audit = bundle["audit"]
    readme = bundle["readme"]
    lakefile = bundle["lakefile"]
    manifest = bundle["manifest"]
    toolchain = bundle["toolchain"]
    gitignore = bundle["gitignore"]

    for anchor in SOURCE_ANCHORS:
        require(source.count(anchor) == 1, f"source boundary changed: {anchor!r}")

    require(lean.count(MAIN_SIGNATURE) == 1, "exact main declaration changed or duplicated")
    require(lean.count("theorem completeFiberIntersection") == 1, "unexpected theorem alias or duplicate")
    require("STATEMENT_TARGET_UNPROVED" not in lean, "historical unproved target name remains")
    for anchor in PROOF_ANCHORS:
        require(lean.count(anchor) == 1, f"proof anchor changed: {anchor!r}")
    require(
        re.search(r"\b(?:sorry|admit|axiom|opaque|sorryAx|native_decide)\b", lean) is None,
        "placeholder, custom axiom, opaque declaration, or native_decide found",
    )
    require(
        lean.count("variable {F : Type*} [Field F]") == 1
        and lean.count("local instance : DecidableEq F := Classical.decEq F") == 1,
        "field wrapper or local decidable-equality elaboration instance changed",
    )

    for anchor in AUDIT_ANCHORS:
        require(audit.count(anchor) == 1, f"audit boundary changed: {anchor!r}")
    for anchor in README_ANCHORS:
        require(readme.count(anchor) == 1, f"README boundary changed: {anchor!r}")

    require(
        lakefile == """name = "dyadic_complete_fiber_slicing"
defaultTargets = ["DyadicCompleteFiberSlicingTarget"]

[[require]]
name = "mathlib"
git = "https://github.com/leanprover-community/mathlib4.git"
rev = "v4.28.0"

[[lean_lib]]
name = "DyadicCompleteFiberSlicingTarget"
roots = ["DyadicCompleteFiberSlicingTarget"]
""",
        "Lake root/library lock changed",
    )
    require(toolchain == "leanprover/lean4:v4.28.0\n", "Lean toolchain lock changed")
    require(gitignore == "/.lake/\n", "package build-artifact ignore changed")
    require(
        manifest.count('"rev": "8f9d9cff6bd728b17a24e163c9402775d9e6a365"') == 1
        and manifest.count('"inputRev": "v4.28.0"') == 2
        and '"name": "dyadic_complete_fiber_slicing"' in manifest,
        "Mathlib manifest pin or package identity changed",
    )
    return checks


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise VerificationError(f"tamper target is not unique: {old!r}")
    return text.replace(old, new, 1)


def tamper_selftest(bundle: Dict[str, str]) -> int:
    mutations: Sequence[tuple[str, Callable[[Dict[str, str]], None]]] = (
        (
            "source status",
            lambda b: b.__setitem__(
                "source", replace_once(b["source"], "official score remains `0/2`", "official score is `2/2`")
            ),
        ),
        (
            "source intersection ceiling",
            lambda b: b.__setitem__(
                "source",
                replace_once(
                    b["source"],
                    "floor((K-1)/c)` common canonical",
                    "ceil((K-1)/c)` common canonical",
                ),
            ),
        ),
        (
            "main theorem name",
            lambda b: b.__setitem__(
                "lean", replace_once(b["lean"], "theorem completeFiberIntersection", "theorem completeFiberUnion")
            ),
        ),
        (
            "range wrapper",
            lambda b: b.__setitem__(
                "lean", replace_once(b["lean"], "1 ≤ K ∧ K ≤ m ∧ m ≤ n", "1 < K ∧ K ≤ m ∧ m ≤ n")
            ),
        ),
        (
            "divisor wrapper",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "(hrange : 1 ≤ K ∧ K ≤ m ∧ m ≤ n)\n    (hc : c ∣ n)",
                    "(hrange : 1 ≤ K ∧ K ≤ m ∧ m ≤ n)\n    (hc : c < n)",
                ),
            ),
        ),
        (
            "conclusion denominator",
            lambda b: b.__setitem__(
                "lean", replace_once(b["lean"], "(K - 1) / c := by", "(K - 1) / (c + 1) := by")
            ),
        ),
        (
            "power kernel",
            lambda b: b.__setitem__(
                "lean", replace_once(b["lean"], "IsCyclic.card_powMonoidHom_ker H c", "IsCyclic.card_powMonoidHom_ker H (c + 1)")
            ),
        ),
        (
            "root polynomial",
            lambda b: b.__setitem__(
                "lean", replace_once(b["lean"], "(P - Q).roots", "(P + Q).roots")
            ),
        ),
        (
            "proof placeholder",
            lambda b: b.__setitem__(
                "lean", replace_once(b["lean"], "  classical\n  let common", "  sorry\n  classical\n  let common")
            ),
        ),
        (
            "custom axiom",
            lambda b: b.__setitem__("lean", "axiom hiddenFiberBound : False\n" + b["lean"]),
        ),
        (
            "hidden section assumption",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "noncomputable section\n\nvariable {F : Type*} [Field F]",
                    "noncomputable section\n\nclass HiddenAssumption : Prop where out : False\n"
                    "variable [HiddenAssumption]\n\nvariable {F : Type*} [Field F]",
                ),
            ),
        ),
        (
            "drop local decidable equality",
            lambda b: b.__setitem__(
                "lean", replace_once(b["lean"], "local instance : DecidableEq F := Classical.decEq F\n", "")
            ),
        ),
        (
            "audit axiom boundary",
            lambda b: b.__setitem__(
                "audit", replace_once(b["audit"], "[propext, Classical.choice, Quot.sound]", "[sorryAx]")
            ),
        ),
        (
            "audit scope boundary",
            lambda b: b.__setitem__(
                "audit", replace_once(b["audit"], "certifies source equation (1) only", "certifies equations (1)--(3)")
            ),
        ),
        (
            "README residual claim",
            lambda b: b.__setitem__(
                "readme", replace_once(b["readme"], "the residual\n`1792`-profile cap", "the proved residual\n`1792`-profile cap")
            ),
        ),
        (
            "drop package root",
            lambda b: b.__setitem__(
                "lakefile", replace_once(b["lakefile"], 'roots = ["DyadicCompleteFiberSlicingTarget"]\n', "")
            ),
        ),
        (
            "change Mathlib revision",
            lambda b: b.__setitem__(
                "manifest", replace_once(b["manifest"], "8f9d9cff6bd728b17a24e163c9402775d9e6a365", "0" * 40)
            ),
        ),
        (
            "change Lean toolchain",
            lambda b: b.__setitem__(
                "toolchain", replace_once(b["toolchain"], "v4.28.0", "v4.27.0")
            ),
        ),
        (
            "unignore build artifacts",
            lambda b: b.__setitem__("gitignore", ""),
        ),
    )
    caught = 0
    for name, mutate in mutations:
        altered = copy.deepcopy(bundle)
        mutate(altered)
        try:
            verify_bundle(altered)
        except VerificationError:
            caught += 1
        else:
            raise VerificationError(f"tamper was not detected: {name}")
    if caught != len(mutations):
        raise VerificationError("tamper suite did not run completely")
    return caught


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    if not args.check and not args.tamper_selftest:
        parser.error("pass --check and/or --tamper-selftest")
    try:
        bundle = read_bundle()
        checks = verify_bundle(bundle)
        if args.tamper_selftest:
            caught = tamper_selftest(bundle)
            print(f"tamper-selftest: caught {caught}/{caught}")
        print(f"RESULT: PASS ({checks}/{checks})")
        return 0
    except VerificationError as error:
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
