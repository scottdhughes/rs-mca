#!/usr/bin/env python3
"""Fail-closed checks for the rooted-emission cardinality Lean wrapper."""

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
SOURCE_PATH = ROOT / "experimental/notes/thresholds/route_d_rooted_emission_no_go.md"
LEAN_PATH = ROOT / (
    "experimental/lean/kb_rowsharp_route_d_rooted_emission_no_go/"
    "KbRowsharpRouteDRootedEmissionNoGo.lean"
)
README_PATH = ROOT / "experimental/lean/kb_rowsharp_route_d_rooted_emission_no_go/README.md"
AUDIT_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "route_d_rooted_emission_cardinality_formalization.md"
)

SOURCE_SHA256 = "5ec49faba4f3d933319b519538cc481da2eef5bfbeacc61e167810fd119e29f8"

SOURCE_ANCHORS = (
    "STATUS: COUNTEREXAMPLE",
    "## Minimal viable rooted-emission lemma",
    "V_z -> Z_rankdrop(f_z,g_z) times F_p.",
    "The existing owner then gives",
    "The Lean package now also proves only the final finite-\n"
    "envelope consequence of the minimal viable lemma",
    "It does not construct or validate that injection,",
)

LEAN_SIGNATURE = """theorem rootedEmission_fixedLine_cardinality_of_injective
    (p t : Nat) (z : Nat × Nat)
    (deletions : NamedFirstMatchDeletions)
    (lineOf : MarkedSupport → Nat)
    (targetOf : MarkedSupport → Nat × Nat)
    (ambient residual : List MarkedSupport)
    (hExact : IsExactFixedLineResidual deletions lineOf targetOf
      fixedGExponent z ambient residual)
    (emit : MarkedSupport → Fin t × Fin p)
    (markDecoder : Fin t × Fin p → List Nat)
    (hMarkPreserving : ∀ x ∈ residual, markDecoder (emit x) = x.commonCore)
    (hInjective : InjectiveOnResidual residual emit) :
    residual.length ≤ t * p := by"""

COMPAT_SIGNATURE = """theorem rootedEmission_fixedLine_target_unproved
    (p t : Nat) (z : Nat × Nat)
    (deletions : NamedFirstMatchDeletions)
    (lineOf : MarkedSupport → Nat)
    (targetOf : MarkedSupport → Nat × Nat)
    (ambient residual : List MarkedSupport)
    (hExact : IsExactFixedLineResidual deletions lineOf targetOf
      fixedGExponent z ambient residual)
    (emit : MarkedSupport → Fin t × Fin p)
    (markDecoder : Fin t × Fin p → List Nat)
    (hMarkPreserving : ∀ x ∈ residual, markDecoder (emit x) = x.commonCore)
    (hInjective : InjectiveOnResidual residual emit) :
    residual.length ≤ t * p := by"""

PROOF_ANCHORS = (
    "let code : MarkedSupport → Nat := fun x =>",
    "Nat.add_lt_add_left (emit x).2.isLt _",
    "Nat.mul_left_cancel hp hmul",
    "hExact.1.imp_of_mem fun hx hy hxy hcode =>",
    "hInjective hx hy (code_eq_emit_eq hcode)",
    "have hTail : xs ⊆ ys.eraseP (fun a => a == x) := by",
    "List.length_eraseP_of_mem",
    "(List.range (t * p)) codesNodup codesSubset",
    "exact rootedEmission_fixedLine_cardinality_of_injective",
)

README_ANCHORS = (
    "3404d21b64c876c6d9b995ad3e29d7120ab27a54",
    "route_d_rooted_emission_no_go.md",
    "rootedEmission_fixedLine_cardinality_of_injective` | PROVED",
    "rootedEmission_fixedLine_target_unproved` | PROVED COMPATIBILITY ALIAS",
    "Its\nload-bearing hypotheses are `hExact.1` and `hInjective`",
    "integrated-stub interface continuity and boundary visibility",
    "does not identify\n`Fin t` with `Z_rankdrop` or prove `|Z_rankdrop| ≤ t`",
    "does not execute or\nvalidate the eight first-match deletions",
    "The `commonCore` decoder is not a\ndecoder for the complete deployed marked key",
    "proves no global Route-D\npayment, deployed row, or threshold",
    "The source packet remains a\n`COUNTEREXAMPLE`",
)

AUDIT_ANCHORS = (
    "## Status\n\nPROVED",
    "Holm\nBuar's source packet PR #913",
    "rank-drop owner contract is due to Scott Hughes",
    "marked\ntop-seam packet interface cited by the source note is due to Vadim Avdeev",
    "Encode a pair `(i,j) : Fin t × Fin p` as `p*i + j`",
    "Remainder modulo `p`\nrecovers `j`, and cancellation of the positive factor `p` then recovers `i`",
    "The load-bearing Lean hypotheses are exactly `hExact.1`",
    "`hExact.2` and `hMarkPreserving` are deliberately carried",
    "proof-unused",
    "Critical nonclaims:",
    "does not construct or validate the emission",
    "does not repair the\nsource packet's rooted-incidence interface gap",
)


def read_bundle() -> Dict[str, str]:
    paths = {
        "source": SOURCE_PATH,
        "lean": LEAN_PATH,
        "readme": README_PATH,
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
    readme = bundle["readme"]
    audit = bundle["audit"]

    require(
        hashlib.sha256(source.encode("utf-8")).hexdigest() == SOURCE_SHA256,
        "pinned source note changed",
    )
    for anchor in SOURCE_ANCHORS:
        require(
            source.count(anchor) == 1,
            f"source anchor missing or duplicated: {anchor!r}",
        )
    require(
        lean.count(LEAN_SIGNATURE) == 1,
        "exact Lean declaration changed or duplicated",
    )
    require(
        lean.count(COMPAT_SIGNATURE) == 1,
        "original compatibility declaration changed or duplicated",
    )
    for anchor in PROOF_ANCHORS:
        require(
            lean.count(anchor) == 1,
            f"proof anchor missing or duplicated: {anchor!r}",
        )
    require(
        re.search(r"\b(?:sorry|admit|axiom|opaque|sorryAx)\b", lean) is None,
        "declaration-level placeholder or added axiom found",
    )
    for anchor in README_ANCHORS:
        require(
            readme.count(anchor) == 1,
            f"README boundary anchor changed: {anchor!r}",
        )
    for anchor in AUDIT_ANCHORS:
        require(
            audit.count(anchor) == 1,
            f"audit boundary anchor changed: {anchor!r}",
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
                "source",
                replace_once(
                    b["source"], "STATUS: COUNTEREXAMPLE", "STATUS: PROVED"
                ),
            ),
        ),
        (
            "source injection contract",
            lambda b: b.__setitem__(
                "source",
                replace_once(
                    b["source"],
                    "construct an actual finite slope",
                    "select an abstract finite slope",
                ),
            ),
        ),
        (
            "rename theorem",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "theorem rootedEmission_fixedLine_cardinality_of_injective",
                    "theorem rootedEmission_fixedLine_cardinality",
                ),
            ),
        ),
        (
            "change emission envelope",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    LEAN_SIGNATURE,
                    LEAN_SIGNATURE.replace(
                        "(emit : MarkedSupport → Fin t × Fin p)",
                        "(emit : MarkedSupport → Fin (t + 1) × Fin p)",
                    ),
                ),
            ),
        ),
        (
            "remove compatibility declaration",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "theorem rootedEmission_fixedLine_target_unproved",
                    "theorem rootedEmission_fixedLine_target_legacy",
                ),
            ),
        ),
        (
            "drop exact nodup source",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "hExact.1.imp_of_mem fun hx hy hxy hcode =>",
                    "hExact.2.imp_of_mem fun hx hy hxy hcode =>",
                ),
            ),
        ),
        (
            "drop residual injectivity",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "hInjective hx hy (code_eq_emit_eq hcode)",
                    "code_eq_emit_eq hcode",
                ),
            ),
        ),
        (
            "change range bound",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "(residual.map code) (List.range (t * p)) codesNodup codesSubset",
                    "(residual.map code) (List.range (t + p)) codesNodup codesSubset",
                ),
            ),
        ),
        (
            "insert placeholder",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "  let code : MarkedSupport → Nat := fun x =>\n",
                    "  sorry\n  let code : MarkedSupport → Nat := fun x =>\n",
                ),
            ),
        ),
        (
            "insert inline placeholder",
            lambda b: b.__setitem__(
                "lean",
                replace_once(
                    b["lean"],
                    "induction xs with\n    | nil => simp\n    | cons x xs ih",
                    "induction xs with\n    | nil => exact by sorry\n    | cons x xs ih",
                ),
            ),
        ),
        (
            "insert private axiom",
            lambda b: b.__setitem__(
                "lean",
                "private axiom hiddenFalse : False\n" + b["lean"],
            ),
        ),
        (
            "README status",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "rootedEmission_fixedLine_cardinality_of_injective` | PROVED",
                    "rootedEmission_fixedLine_cardinality_of_injective` | STUB_ONLY",
                ),
            ),
        ),
        (
            "stub-continuity boundary",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "integrated-stub interface continuity and boundary visibility",
                    "direct source-interface fidelity",
                ),
            ),
        ),
        (
            "source commit pin",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "3404d21b64c876c6d9b995ad3e29d7120ab27a54",
                    "0000000000000000000000000000000000000000",
                ),
            ),
        ),
        (
            "source label",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "route_d_rooted_emission_no_go.md",
                    "route_d_rooted_emission.md",
                ),
            ),
        ),
        (
            "Holm credit",
            lambda b: b.__setitem__(
                "audit",
                replace_once(b["audit"], "Holm\nBuar's", "The source packet's"),
            ),
        ),
        (
            "Scott credit",
            lambda b: b.__setitem__(
                "audit",
                replace_once(b["audit"], "due to Scott Hughes", "integrated"),
            ),
        ),
        (
            "Vadim credit",
            lambda b: b.__setitem__(
                "audit",
                replace_once(b["audit"], "due to Vadim Avdeev", "integrated"),
            ),
        ),
        (
            "rank-drop identification boundary",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "does not identify\n`Fin t` with `Z_rankdrop`",
                    "identifies\n`Fin t` with `Z_rankdrop`",
                ),
            ),
        ),
        (
            "executable deletion boundary",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "does not execute or\nvalidate the eight first-match deletions",
                    "executes and\nvalidates the eight first-match deletions",
                ),
            ),
        ),
        (
            "complete-key boundary",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "not a\ndecoder for the complete deployed marked key",
                    "a\ndecoder for the complete deployed marked key",
                ),
            ),
        ),
        (
            "global-payment boundary",
            lambda b: b.__setitem__(
                "readme",
                replace_once(
                    b["readme"],
                    "proves no global Route-D\npayment, deployed row, or threshold",
                    "proves a global Route-D\npayment, deployed row, and threshold",
                ),
            ),
        ),
        (
            "proof-unused boundary",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "proof-unused",
                    "used to establish the inequality",
                ),
            ),
        ),
        (
            "proof encoding description",
            lambda b: b.__setitem__(
                "audit",
                replace_once(
                    b["audit"],
                    "Encode a pair `(i,j) : Fin t × Fin p` as `p*i + j`",
                    "Encode a pair `(i,j) : Fin t × Fin p` as `i + t*j`",
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
