#!/usr/bin/env python3
"""Fail-closed source/proof checks for the C3 divisor-sigma Lean theorem."""

from __future__ import annotations

import argparse
import copy
import hashlib
import re
import sys
from pathlib import Path
from typing import Callable, Dict, Sequence


class VerificationError(RuntimeError):
    """A source, statement, proof-boundary, or tamper check failed."""


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = ROOT / "experimental/notes/thresholds/c3_planted_divisor_census.md"
LEAN_PATH = ROOT / (
    "experimental/lean/first_match_atlas/"
    "FirstMatchAtlas/PlantedDivisorCensus.lean"
)
ROOT_MODULE_PATH = ROOT / "experimental/lean/first_match_atlas/FirstMatchAtlas.lean"
AUDIT_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "c3_planted_divisor_sigma_formalization.md"
)

SOURCE_SHA256 = "f36f66cc8672cc6b7ae653d8868ce98283e31a50f371812f7c264d121523711f"
LEAN_SHA256 = "0d0c6305a351a910f4fc0499e924cbe1d3a265a096d3585a0ca67cb17c1ca76b"
AUDIT_SHA256 = "a2531f9db8df0b659e4208716d5b64f7523b7d83fa02ecaeab80a02607337ad7"

MAIN_SIGNATURE = """theorem sigmaOf_le_mul_one_add_log2 :
    ∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N) := by"""

ASYMPTOTIC_ALIAS = """theorem sigmaOf_subexponential :
    ∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N) :=
  sigmaOf_le_mul_one_add_log2"""

HISTORICAL_ALIAS = """theorem sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED :
    ∀ N : Nat, N ≥ 1 → sigmaOf N ≤ N * (1 + Nat.log2 N) :=
  sigmaOf_le_mul_one_add_log2"""

SOURCE_ANCHORS = (
    "C3 VERDICT:\nPARTIAL",
    "Lean proof at\n`experimental/lean/first_match_atlas/FirstMatchAtlas/PlantedDivisorCensus.lean`",
    "Its discrete `Nat.log2` theorem is proved\ndirectly by dyadic denominator blocks",
    "No claim that the Lean theorem proves the real-valued formula",
    "Since `Nat.log2` is floored, neither statement is presented as a formal\n  consequence of the other.",
    "`sigmaOf_le_mul_one_add_log2`:",
    "`sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED` remain as proved",
    "not a formalization of the source note's real-analysis formula,\nasymptotic notation, or the bridge to `e^{o(N)}`",
    "the floor matters (already at `N=3`)",
    "# -> RESULT: PASS (82/82)",
)

PROOF_ANCHORS = (
    "private theorem sum_map_le_of_nodup_subset",
    "private theorem divisor_data",
    "simp only [Nat.dvd_iff_mod_eq_zero]",
    "private theorem complement_data",
    "have hfactor : N / d * d = N := Nat.div_mul_cancel hd.2.2",
    "apply (Nat.div_eq_iff_eq_mul_left hqpos hqdvd).2",
    "private theorem complement_injective_on_divisors",
    "private theorem sigma_le_harmonic_floor",
    "private def dyadicDenoms",
    "private theorem dyadic_block_sum_le",
    "Nat.le_trans hsum (Nat.mul_div_le N (2 ^ level))",
    "private theorem dyadic_sum_le",
    "exact Nat.lt_of_le_of_lt (by omega) Nat.lt_log2_self",
    "private theorem harmonic_floor_le_log2",
    "intro N _hN",
    "exact Nat.le_trans (sigma_le_harmonic_floor N)",
)

AUDIT_ANCHORS = (
    "## Status\n\nPROVED",
    "`FirstMatchAtlas.PlantedDivisorCensus.sigmaOf_le_mul_one_add_log2`",
    "the Lean proof also establishes the inequality at\n`N = 0`",
    "It does not formalize the source note's real-valued formula",
    "`Nat.log2` is floored, so that shortcut is invalid",
    "For every divisor `d` of `N`, take the complementary divisor `q = N/d`",
    "Block `j` has exactly `2^j` entries",
    "`[propext, Classical.choice, Quot.sound]`",
    "none of the declarations depends on\n`sorryAx` or a custom axiom",
    "It does not change the source packet's overall `PARTIAL` verdict",
    "Lean does not prove the general identity\n`cosetCensusTotal N = sigmaOf N`",
    "asymptotic notation, or the bridge to\n`e^{o(N)}`",
    "does not census row-dependent common factors",
    "pay C7, C8, or C9",
    "prove a witness-exhaustive atlas",
    "an MCA threshold or prize claim",
)


def read_bundle() -> Dict[str, str]:
    paths = {
        "source": SOURCE_PATH,
        "lean": LEAN_PATH,
        "root_module": ROOT_MODULE_PATH,
        "audit": AUDIT_PATH,
    }
    bundle: Dict[str, str] = {}
    for key, path in paths.items():
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

    source = bundle["source"]
    lean = bundle["lean"]
    root_module = bundle["root_module"]
    audit = bundle["audit"]

    require(
        hashlib.sha256(source.encode("utf-8")).hexdigest() == SOURCE_SHA256,
        "pinned source note changed",
    )
    require(
        hashlib.sha256(lean.encode("utf-8")).hexdigest() == LEAN_SHA256,
        "pinned Lean implementation changed",
    )
    require(
        hashlib.sha256(audit.encode("utf-8")).hexdigest() == AUDIT_SHA256,
        "pinned formalization note changed",
    )
    require(
        root_module.startswith("import FirstMatchAtlas.PlantedDivisorCensus\n")
        and root_module.count("import FirstMatchAtlas.PlantedDivisorCensus") == 1,
        "package root no longer imports the planted-divisor module exactly once",
    )
    for anchor in SOURCE_ANCHORS:
        require(
            source.count(anchor) == 1,
            f"source boundary missing or duplicated: {anchor!r}",
        )

    require(
        lean.count(MAIN_SIGNATURE) == 1,
        "exact main Lean declaration changed or duplicated",
    )
    require(
        lean.count(ASYMPTOTIC_ALIAS) == 1,
        "asymptotic-facing compatibility alias changed or duplicated",
    )
    require(
        lean.count(HISTORICAL_ALIAS) == 1,
        "historical compatibility alias changed or duplicated",
    )
    for anchor in PROOF_ANCHORS:
        require(
            lean.count(anchor) == 1,
            f"proof anchor missing or duplicated: {anchor!r}",
        )
    require(
        re.search(r"\b(?:sorry|admit|axiom|opaque|sorryAx)\b", lean) is None,
        "placeholder or declaration-level custom axiom found",
    )

    for anchor in AUDIT_ANCHORS:
        require(
            audit.count(anchor) == 1,
            f"audit boundary missing or duplicated: {anchor!r}",
        )
    return checks


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise VerificationError(f"tamper target is not unique: {old!r}")
    return text.replace(old, new, 1)


def tamper_selftest(bundle: Dict[str, str]) -> int:
    mutations: Sequence[tuple[str, Callable[[Dict[str, str]], None]]] = (
        (
            "source verdict",
            lambda b: b.__setitem__(
                "source", replace_once(b["source"], "C3 VERDICT:\nPARTIAL", "C3 VERDICT:\nPROVED")
            ),
        ),
        (
            "source real-log boundary",
            lambda b: b.__setitem__(
                "source",
                replace_once(
                    b["source"],
                    "No claim that the Lean theorem proves the real-valued formula",
                    "The Lean theorem proves the real-valued formula",
                ),
            ),
        ),
        (
            "main theorem name",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "theorem sigmaOf_le_mul_one_add_log2 :",
                    "theorem sigmaOf_logarithmic_bound :",
                ),
            ),
        ),
        (
            "source wrapper",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    MAIN_SIGNATURE,
                    MAIN_SIGNATURE.replace("N ≥ 1", "N ≥ 2"),
                ),
            ),
        ),
        (
            "target rhs",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    MAIN_SIGNATURE,
                    MAIN_SIGNATURE.replace("1 + Nat.log2 N", "2 + Nat.log2 N"),
                ),
            ),
        ),
        (
            "complement recovery",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "apply (Nat.div_eq_iff_eq_mul_left hqpos hqdvd).2",
                    "apply (Nat.div_eq_iff_eq_mul_right hqpos hqdvd).2",
                ),
            ),
        ),
        (
            "dyadic block payment",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "Nat.le_trans hsum (Nat.mul_div_le N (2 ^ level))",
                    "Nat.le_trans hsum (Nat.mul_div_le N (2 ^ (level + 1)))",
                ),
            ),
        ),
        (
            "log2 cover",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "exact Nat.lt_of_le_of_lt (by omega) Nat.lt_log2_self",
                    "exact Nat.lt_of_le_of_lt (by omega) Nat.log2_self_le",
                ),
            ),
        ),
        (
            "asymptotic alias target",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"], ASYMPTOTIC_ALIAS, ASYMPTOTIC_ALIAS.replace("sigmaOf N", "sigmaOf (N + 1)")
                ),
            ),
        ),
        (
            "historical alias removed",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "theorem sigmaOf_subexponential_STATEMENT_TARGET_UNPROVED :",
                    "theorem sigmaOf_subexponential_STATEMENT_TARGET :",
                ),
            ),
        ),
        (
            "insert proof placeholder",
            lambda b: b.__setitem__(
                "lean",
                replace_once(b["lean"], "  intro N _hN\n", "  sorry\n  intro N _hN\n"),
            ),
        ),
        (
            "insert inline placeholder",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "| zero => simp [dyadicDenoms]",
                    "| zero => exact by sorry",
                ),
            ),
        ),
        (
            "insert private axiom",
            lambda b: b.__setitem__(
                "lean", "private axiom hiddenSigmaBound : False\n" + b["lean"]
            ),
        ),
        (
            "insert hidden section assumption",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "namespace FirstMatchAtlas.PlantedDivisorCensus\n",
                    "class HiddenAssumption : Prop where\n"
                    "  out : False\n\n"
                    "variable [hiddenAssumption : HiddenAssumption]\n"
                    "include hiddenAssumption\n\n"
                    "namespace FirstMatchAtlas.PlantedDivisorCensus\n",
                ),
            ),
        ),
        (
            "drop package-root import",
            lambda b: b.__setitem__(
                "root_module",
                replace_once(
                    b["root_module"],
                    "import FirstMatchAtlas.PlantedDivisorCensus\n",
                    "",
                ),
            ),
        ),
        (
            "audit status",
            lambda b: b.__setitem__(
                "audit", replace_once(b["audit"], "## Status\n\nPROVED", "## Status\n\nCONDITIONAL")
            ),
        ),
        (
            "audit coset identity boundary",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "Lean does not prove the general identity",
                    "Lean proves the general identity",
                ),
            ),
        ),
        (
            "audit asymptotic boundary",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "asymptotic notation, or the bridge to",
                    "asymptotic notation and the bridge to",
                ),
            ),
        ),
        (
            "audit row-dependent boundary",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "does not census row-dependent common factors",
                    "censuses row-dependent common factors",
                ),
            ),
        ),
        (
            "audit all-parameter boundary",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "prove the dihedral or ramification statements for\nall parameters",
                    "proves the dihedral and ramification statements for\nall parameters",
                ),
            ),
        ),
        (
            "audit atlas boundary",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "prove a witness-exhaustive atlas",
                    "proves a witness-exhaustive atlas",
                ),
            ),
        ),
        (
            "audit threshold boundary",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "an MCA threshold or prize claim",
                    "an MCA threshold and prize claim",
                ),
            ),
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
