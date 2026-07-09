#!/usr/bin/env python3
"""
Gate the Grande Finale Lean <-> grande_finale.tex correspondence audit.

Note: experimental/notes/audits/lean_grande_finale_correspondence_audit.md
Tex:  experimental/grande_finale.tex
Lean: experimental/lean/grande_finale/{GrandeFinale.lean, GrandeFinale/*.lean}

Zero-arg, stdlib-only, exit 0 = PASS.  Discharges the maintainer's asked step
("Audit correspondence between the Lean declaration docstrings and the labels in
experimental/grande_finale.tex"): a TEXTUAL audit only.  lake build is NOT run
here (Mathlib-pinned toolchain unavailable; the package README forbids casual
builds); native_decide constants are numerically cross-checked, not re-executed.

Gate groups and claim labels mirror the note:

  VERIFIED-CLEAN   real labels present in the tex at the claimed sections;
                   per-file declaration counts; sorry/admit/axiom == 0.
  DRIFT-FOUND      TEX-SIDE (hard, must always hold): each phantom label is
                   ABSENT from the tex as a complete label token, and the two
                   phantom manuscript files are absent from the repo.
                   LEAN-SIDE (state, passes in BOTH states): each phantom label's
                   presence in the .lean file(s) the note names.  If the
                   maintainer fixes the docstrings these flip from DRIFT-PRESENT
                   to DRIFT-FIXED; the exit-0 contract holds either way and the
                   run prints which world it is in.  A phantom that vanished from
                   the named files but reappeared elsewhere (DRIFT-MOVED) fails:
                   that means the audit's file list went stale.
  AUDIT (native)   the 12 native_decide numeric literals equal their tex decimals.

Boundary-aware matching: the tex contains the string "thm:asymptotic" only as a
prefix of the real label "thm:asymptotic-rs-mca-closure-combined".  The phantom
token check excludes a trailing hyphen/word-char so a prefix is never miscounted
as the phantom label being present (tamper self-test #4 guards this).

Memory-safe by construction: pure text processing.  main() reads each file once
into a string (all are small; the tex is ~2.4k lines) and never builds large
derived structures; internal tamper copies never touch repo files.
"""
import os
import re
import sys

CHECKS = 0
FAILS = []


def gate(name, ok, detail=""):
    """Record one hard check.  ok must be truthy to PASS."""
    global CHECKS
    CHECKS += 1
    ok = bool(ok)
    if not ok:
        FAILS.append(f"{name}: {detail or 'condition false'}")
    print(f"  [{'ok' if ok else 'XX'}] {name}{('  ' + detail) if detail else ''}")
    return ok


# ---------------------------------------------------------------------------
# repo file access  (script lives at experimental/scripts/<this>.py)
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(_HERE))            # .../<repo root>
TEX_REL = "experimental/grande_finale.tex"
LEAN_REL = "experimental/lean/grande_finale"
ALL_LEAN = [
    "GrandeFinale.lean", "Main.lean",
    "GrandeFinale/BC.lean", "GrandeFinale/SP.lean", "GrandeFinale/Frontier.lean",
    "GrandeFinale/QEntropyInverse.lean", "GrandeFinale/QFourierTao.lean",
    "GrandeFinale/QPrimitiveCollision.lean",
]


def read(rel):
    p = os.path.join(REPO, rel)
    if not os.path.exists(p):
        raise SystemExit(f"missing file: {p}\n(run from any dir; script self-locates the repo root)")
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def read_lean(name):
    return read(os.path.join(LEAN_REL, name))


# ---------------------------------------------------------------------------
# boundary-aware "complete label token" matcher
# ---------------------------------------------------------------------------
def token_present(text, label):
    """True iff `label` appears as a complete token (not extended by a
    hyphen/word-char on either side).  Case-insensitive."""
    pat = re.compile(r"(?<![\w:-])" + re.escape(label) + r"(?![\w-])", re.IGNORECASE)
    return pat.search(text) is not None


def token_count(text, label):
    pat = re.compile(r"(?<![\w:-])" + re.escape(label) + r"(?![\w-])", re.IGNORECASE)
    return len(pat.findall(text))


# ---------------------------------------------------------------------------
# audit facts (measured at b99b2c4; pinned so future drift is caught)
# ---------------------------------------------------------------------------
# phantom label -> .lean file(s) the note names as citing it
PHANTOM_LABELS = {
    "conj:Q": ["GrandeFinale/QEntropyInverse.lean", "GrandeFinale/QFourierTao.lean", "GrandeFinale/SP.lean"],
    "conj:SP": ["GrandeFinale/SP.lean"],
    "conj:BC": ["GrandeFinale/BC.lean"],
    "thm:asymptotic": ["GrandeFinale/SP.lean"],
    "lem:log-moment-to-q": ["GrandeFinale/QFourierTao.lean"],
    "cor:asymp-q-fourier-tao": ["GrandeFinale/QFourierTao.lean"],
    "thm:primitive-log-collision": ["GrandeFinale/QFourierTao.lean", "GrandeFinale/QPrimitiveCollision.lean"],
}

# manuscript files cited in .lean headers that exist nowhere in the repo
PHANTOM_FILES = ["q_fourier_tao_finish_patch.tex", "grande_finale_bc_attempt.tex"]

# real replacement label -> pinned \label{...} line in the tex (checked +-40)
REAL_LABELS = {
    "thm:logmoment-equivalence": 773,
    "def:primitive-logmoment": 756,
    "prop:vandermonde-kills-low-rank": 876,
    "prop:moment-sandwich": 709,
    "thm:moment-q": 725,
    "thm:q-implies-sp": 1889,
    "prop:q-moment-order-floor": 2093,
    "prob:row-sharp-q": 2177,
}

# declaration-count rule: lines matching ^(theorem|lemma|def|noncomputable def) + space
DECL_RE = re.compile(r"^(theorem|lemma|def|noncomputable def) ")
DECL_COUNTS = {
    "GrandeFinale.lean": 39,
    "GrandeFinale/BC.lean": 25,
    "GrandeFinale/SP.lean": 19,
    "GrandeFinale/Frontier.lean": 14,
    "GrandeFinale/QEntropyInverse.lean": 5,
    "GrandeFinale/QFourierTao.lean": 5,
    "GrandeFinale/QPrimitiveCollision.lean": 5,
}
DECL_TOTAL = 112

# 12 native_decide literals: (name, value, lean file, tex-window or None=anywhere).
# The field primes pKB/pM31 are symbolic in the tex, so excluded.
NATIVE_DECIDE = [
    ("BstarKB",            "274980728111395087",    "GrandeFinale.lean", None),
    ("BstarM31",           "16777215",              "GrandeFinale.lean", None),
    ("M_KB_a0",            "138634741058327852652", "GrandeFinale.lean", None),
    ("M_KB_a0p",           "57198030366",           "GrandeFinale.lean", None),
    ("M_M31_a0",           "4281388998575706",      "GrandeFinale.lean", None),
    ("M_M31_a0p",          "1752700",               "GrandeFinale.lean", None),
    ("M31_watch",          "12769758",              "GrandeFinale.lean", None),
    ("bc_pencil_num",      "2097152",               "GrandeFinale/BC.lean", None),
    ("bc_KB_omega",        "980104",                "GrandeFinale/BC.lean", None),
    ("bc_M31_omega",       "980128",                "GrandeFinale/BC.lean", None),
    ("mode17_null",        "672",                   "GrandeFinale/Frontier.lean", (985, 1005)),
    ("mode17_nonnull",     "673",                   "GrandeFinale/Frontier.lean", (985, 1005)),
]

SORRY_TOKENS = [("sorry", r"\bsorry\b"), ("admit", r"\badmit\b"), ("axiom", r"\baxiom\b")]


# ---------------------------------------------------------------------------
# gate groups
# ---------------------------------------------------------------------------
def part_tex_phantoms_absent(tex):
    print("-- TEX-SIDE (hard): phantom labels absent from grande_finale.tex --")
    for label in PHANTOM_LABELS:
        n = token_count(tex, label)
        gate(f"tex has NO token '{label}'", n == 0, f"token-hits={n}")


def part_phantom_files_absent():
    print("-- TEX-SIDE (hard): phantom manuscript files absent from repo --")
    for fname in PHANTOM_FILES:
        hits = []
        for dirpath, _dirs, files in os.walk(os.path.join(REPO, "experimental")):
            if fname in files:
                hits.append(os.path.join(dirpath, fname))
        gate(f"no repo file named '{fname}'", not hits, f"found={hits}")


def part_lean_phantom_state():
    """LEAN-SIDE state group: passes in BOTH the drift-present and drift-fixed
    worlds; prints which holds.  Fails only on DRIFT-MOVED (stale file list)."""
    print("-- LEAN-SIDE (state): phantom-label presence in the named .lean files --")
    lean_texts = {name: read_lean(name) for name in ALL_LEAN}
    present = fixed = 0
    for label, named in PHANTOM_LABELS.items():
        in_named = any(token_present(lean_texts[f], label) for f in named)
        in_pkg = any(token_present(t, label) for t in lean_texts.values())
        if in_named:
            state = "DRIFT-PRESENT (finding reproduced)"
            present += 1
            ok = True
        elif not in_pkg:
            state = "DRIFT-FIXED (removed package-wide)"
            fixed += 1
            ok = True
        else:
            state = "DRIFT-MOVED (present elsewhere; audit file list is stale)"
            ok = False
        gate(f"'{label}' state coherent", ok, state)

    total = len(PHANTOM_LABELS)
    if present == total:
        headline = f"FINDING INTACT: {present}/{total} phantom labels still cited in the named Lean files."
    elif fixed == total:
        headline = f"FINDING RESOLVED UPSTREAM: all {total} phantom labels removed; docstrings fixed after the audit."
    else:
        headline = f"FINDING PARTIALLY RESOLVED: {present} still present, {fixed} fixed (of {total})."
    print(f"     >> {headline}")
    gate("phantom-label state tally is complete", present + fixed == total,
         f"present={present} fixed={fixed} total={total}")


def part_real_labels_present(tex_lines):
    print("-- VERIFIED-CLEAN (hard): real replacement labels present at claimed section --")
    for label, pin in REAL_LABELS.items():
        needle = r"\label{" + label + "}"
        found = [i + 1 for i, ln in enumerate(tex_lines) if needle in ln]
        near = [f for f in found if abs(f - pin) <= 40]
        gate(f"tex \\label{{{label}}} within +-40 of L{pin}", bool(near),
             f"found={found}")


def part_sorry_axiom():
    print("-- VERIFIED-CLEAN (hard): sorry / admit / axiom inventory == 0 --")
    joined = "\n".join(read_lean(name) for name in ALL_LEAN)
    for tok, pat in SORRY_TOKENS:
        n = len(re.findall(pat, joined))
        gate(f"package has zero '{tok}'", n == 0, f"count={n}")


def part_decl_counts():
    print("-- VERIFIED-CLEAN (hard): per-file declaration counts --")
    total = 0
    for rel, want in DECL_COUNTS.items():
        got = sum(1 for ln in read_lean(rel).splitlines() if DECL_RE.match(ln))
        total += got
        gate(f"{rel} declarations == {want}", got == want, f"got={got}")
    gate(f"total audited declarations == {DECL_TOTAL}", total == DECL_TOTAL, f"got={total}")


def part_native_decide(tex, tex_lines):
    print("-- AUDIT: 12 native_decide constants equal their tex decimals --")
    for name, value, lean_rel, window in NATIVE_DECIDE:
        in_lean = value in read_lean(lean_rel)
        if window is None:
            in_tex = value in tex
            detail = f"{value}"
        else:
            lo, hi = window
            in_tex = any(value in ln for ln in tex_lines[lo - 1:hi])
            detail = f"{value} (tex L{lo}-{hi})"
        gate(f"{name} lean==tex", in_lean and in_tex, detail)


def part_tamper(tex):
    """Self-tests on INTERNAL string copies only; never touch repo files."""
    print("-- TAMPER self-tests (internal copies) --")
    passed = 0

    # 1. plant a phantom label into a tex copy -> absence check must flag it.
    faked = tex + "\n\\label{conj:Q}\n"
    if token_count(faked, "conj:Q") == 1 and token_count(tex, "conj:Q") == 0:
        passed += 1
        print("  [ok] #1 planted phantom 'conj:Q' in tex copy is detected")
    else:
        FAILS.append("tamper1: planted phantom label not detected")

    # 2. plant a fake sorry in a lean copy -> the inventory must catch it.
    lean_copy = "theorem bogus : True := by sorry\n"
    if len(re.findall(r"\bsorry\b", lean_copy)) == 1:
        passed += 1
        print("  [ok] #2 planted 'sorry' in lean copy is caught")
    else:
        FAILS.append("tamper2: planted sorry not caught")

    # 3. perturb a native_decide constant -> cross-check must fail.
    good = "274980728111395087"
    bad = "274980728111395088"
    if (good in tex) and (bad not in tex):
        passed += 1
        print("  [ok] #3 perturbed BstarKB constant fails the tex match")
    else:
        FAILS.append("tamper3: perturbed constant not caught")

    # 4. boundary-awareness: a phantom PREFIX inside a longer real label must
    #    NOT count as the phantom token being present.
    only_long = "\\cref{thm:asymptotic-rs-mca-closure-combined}"
    if ("thm:asymptotic" in only_long) and (not token_present(only_long, "thm:asymptotic")):
        passed += 1
        print("  [ok] #4 'thm:asymptotic' prefix in a longer label is not a false hit")
    else:
        FAILS.append("tamper4: boundary-aware token match wrong on prefix")

    global CHECKS
    CHECKS += passed
    gate("tamper self-tests caught (>=3)", passed >= 3, f"passed={passed}/4")


# ---------------------------------------------------------------------------
def main():
    tex = read(TEX_REL)
    tex_lines = tex.splitlines()

    part_tex_phantoms_absent(tex)
    part_phantom_files_absent()
    part_lean_phantom_state()
    part_real_labels_present(tex_lines)
    part_sorry_axiom()
    part_decl_counts()
    part_native_decide(tex, tex_lines)
    part_tamper(tex)

    print("=" * 74)
    if FAILS:
        for f in FAILS:
            print("FAIL:", f)
        print(f"RESULT: FAIL ({len(FAILS)} of {CHECKS} checks failed)")
        return 1
    print(f"RESULT: PASS ({CHECKS}/{CHECKS} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
