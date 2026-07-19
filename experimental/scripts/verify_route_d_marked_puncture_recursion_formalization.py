#!/usr/bin/env python3
"""Fail-closed correspondence checks for the marked-puncture Lean wrappers."""

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
SOURCE_PATH = ROOT / "experimental/notes/thresholds/route_d_marked_puncture_contact_recursion_v1.md"
LEAN_PATH = ROOT / (
    "experimental/lean/route_d_marked_puncture_contact_recursion_v1/"
    "RouteDMarkedPunctureContactRecursionV1.lean"
)
README_PATH = ROOT / "experimental/lean/route_d_marked_puncture_contact_recursion_v1/README.md"
AUDIT_PATH = ROOT / "experimental/notes/thresholds/route_d_marked_puncture_recursion_formalization.md"

SOURCE_SHA256 = "a3f4dcc3b09c148d65b18675186e4135b17641969a0923aaa1c723347779888f"

SOURCE_ANCHORS = (
    "STATUS: PROVED",
    "**Theorem 1 (arbitrary-carried-`Q` least-contact bijection).**",
    "**Corollary 2 (conditional hereditary boundary budget).**",
    "The theorem does not assert that any current first-match residual is",
    "The three generic\nlogical/cardinality wrappers are now proved",
)

LEAN_SIGNATURES = (
    """theorem carriedQ_leastContact_erase_insert_equiv
    (parentGood : Parent → Prop) (childGood : Root → Child → Prop)
    (Q : Parent → Prop) (leastContact : Root → Parent → Prop)
    (erase : Root → Parent → Child) (insert : Root → Child → Parent)
    (b : Root)
    (forwardStructural : ∀ S, parentGood S → leastContact b S →
      childGood b (erase b S))
    (backwardStructural : ∀ P, childGood b P →
      parentGood (insert b P) ∧ leastContact b (insert b P))
    (eraseInsert : ∀ P, childGood b P → erase b (insert b P) = P)
    (insertErase : ∀ S, parentGood S → leastContact b S →
      insert b (erase b S) = S) :
    Nonempty (ExactEquiv
      {S : Parent // LeastContactParent parentGood Q leastContact b S}
      {P : Child // CarriedQChild childGood Q insert b P}) := by""",
    """theorem least_contact_partition
    (parentGood : Parent → Prop) (allowed : Root → Prop)
    (precedes : Root → Root → Prop) (touches : Root → Parent → Prop)
    (firstExists : ∀ S, parentGood S → HasBoundaryContact allowed touches S →
      ∃ b, IsLeastContact allowed precedes touches b S)
    (firstUnique : ∀ S b c,
      IsLeastContact allowed precedes touches b S →
      IsLeastContact allowed precedes touches c S → b = c) :
    ∀ S, parentGood S →
      (HasBoundaryContact allowed touches S ↔
        HasUniqueLeastContact allowed precedes touches S) := by""",
    """theorem hereditary_cardinality_bound
    (roots : List Root) (cellCard carriedCard coarseChildCard : Root → Nat)
    (Q : Parent → Prop) (Qchild : Child → Prop)
    (insert : Root → Child → Parent)
    (carriedMember childStructural coarseMember : Root → Child → Prop)
    (carriedHasQ : ∀ b P, carriedMember b P → Q (insert b P))
    (carriedHasStructure : ∀ b P, carriedMember b P → childStructural b P)
    (deletionHereditary : ∀ b P, Q (insert b P) → Qchild P)
    (coarseAccepts : ∀ b P, childStructural b P → Qchild P → coarseMember b P)
    (exactCarriedCard : ∀ b, cellCard b = carriedCard b)
    (inclusionCardBound : ∀ b,
      (∀ P, carriedMember b P → coarseMember b P) →
      carriedCard b ≤ coarseChildCard b) :
    (roots.map cellCard).sum ≤ (roots.map coarseChildCard).sum := by""",
)

PROOF_ANCHORS = (
    "childGood b P ∧ Q (insert b P)",
    "simpa only [insertErase S.1 hParent hLeast] using hQ",
    "exact eraseInsert P.1 P.2.1",
    "exact firstUnique S c b hc hb",
    "exact deletionHereditary b P (carriedHasQ b P hCarried)",
    "simpa using Nat.add_le_add (pointwise b) ih",
)

README_ANCHORS = (
    "carriedQ_leastContact_erase_insert_equiv` | PROVED",
    "least_contact_partition` | PROVED",
    "hereditary_cardinality_bound` | PROVED",
    "They do not\nformalize the source note end to end",
)

AUDIT_ANCHORS = (
    "## Status\n\nPROVED",
    "abstract logical kernels",
    "Critical nonclaims:",
    "produce the root-blind owner",
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
            raise VerificationError(f"cannot read {path.relative_to(ROOT)}: {error}") from error
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
        require(source.count(anchor) == 1, f"source anchor missing or duplicated: {anchor!r}")
    for signature in LEAN_SIGNATURES:
        require(lean.count(signature) == 1, "exact Lean declaration changed or duplicated")
    for anchor in PROOF_ANCHORS:
        require(lean.count(anchor) == 1, f"proof anchor missing or duplicated: {anchor!r}")
    require(
        re.search(r"(?m)^\s*(sorry|admit|axiom|opaque)\b|sorryAx", lean) is None,
        "declaration-level placeholder or added axiom found",
    )
    for anchor in README_ANCHORS:
        require(readme.count(anchor) == 1, f"README boundary anchor changed: {anchor!r}")
    for anchor in AUDIT_ANCHORS:
        require(audit.count(anchor) == 1, f"audit boundary anchor changed: {anchor!r}")
    return checks


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise VerificationError(f"tamper target is not unique: {old!r}")
    return text.replace(old, new, 1)


def tamper_selftest(bundle: Dict[str, str]) -> int:
    mutations: Sequence[tuple[str, Callable[[Dict[str, str]], None]]] = (
        ("source status", lambda b: b.__setitem__(
            "source", replace_once(b["source"], "STATUS: PROVED", "STATUS: CONDITIONAL"))),
        ("source theorem label", lambda b: b.__setitem__(
            "source", replace_once(b["source"], "arbitrary-carried-`Q`", "root-blind-`Q`"))),
        ("erase carried Q", lambda b: b.__setitem__(
            "lean", replace_once(
                b["lean"],
                "childGood b P ∧ Q (insert b P)",
                "childGood b P ∧ Q P"))),
        ("drop inverse law", lambda b: b.__setitem__(
            "lean", replace_once(b["lean"], "exact eraseInsert P.1 P.2.1", "rfl"))),
        ("reverse uniqueness", lambda b: b.__setitem__(
            "lean", replace_once(b["lean"], "firstUnique S c b hc hb", "firstUnique S b c hb hc"))),
        ("drop deletion heredity", lambda b: b.__setitem__(
            "lean", replace_once(
                b["lean"],
                "exact deletionHereditary b P (carriedHasQ b P hCarried)",
                "exact carriedHasQ b P hCarried"))),
        ("insert placeholder", lambda b: b.__setitem__(
            "lean", replace_once(b["lean"], "  intro S hParent\n", "  sorry\n"))),
        ("README status", lambda b: b.__setitem__(
            "readme", replace_once(b["readme"], "least_contact_partition` | PROVED", "least_contact_partition` | STUB_ONLY"))),
        ("erase boundary", lambda b: b.__setitem__(
            "audit", replace_once(b["audit"], "produce the root-blind owner", "supply the root-blind owner"))),
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
