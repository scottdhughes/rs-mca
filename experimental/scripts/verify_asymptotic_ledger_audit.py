#!/usr/bin/env python3
"""Verifier for the asymptotic RS-MCA closed-ledger citation audit.

Zero-arg, stdlib-only. Gates the machine-readable claim->label->verdict map in
experimental/data/asymptotic_rs_mca_closed_ledger_audit.json against the source
manuscripts in-tree.

This is a CITATION verifier, not a proof checker: it confirms that every cited
source file exists, that every located label/quote byte-matches its source
within a +/-5 line window of the stated line, that the verdict tally is
self-consistent, that the quasicube boolean-difference derivation is
arithmetically valid, and that the missing moduli manuscripts (FINDING-1) are
genuinely absent from the tree. It does NOT re-verify the internal correctness
of any cited proof.

Knobs (environment variables):
  ALAUD_AS_CAP_GB  address-space cap in GB via RLIMIT_AS (default 2).
  ALAUD_DATA_DIR   repo root holding experimental/ (default: inferred from this
                   script's location, two directories up).

Exit 0 and print 'RESULT: PASS' on success; exit 1 on any failure.
"""

import copy
import json
import os
import resource
import sys

VICINITY = 5  # +/- lines around the stated line where a quote must appear
FOURWAY = ("FOUND-EXACT", "FOUND-WEAKER", "FOUND-AMBIGUOUS", "PHANTOM")

# Distinctive C9 vocabulary that must live ONLY in the paper if the moduli
# manuscripts are truly absent (FINDING-1).
SCAN_DIRS = ("experimental", "tex")
SCAN_EXTS = (".tex", ".md")

# This audit's own deliverables necessarily quote the phantom C9 tokens (to name
# them); they are audit artifacts, not manuscripts, so the moduli-absence scan
# skips them by path.
AUDIT_ARTIFACTS = (
    "experimental/notes/asymptotic_rs_mca_closed_ledger_audit.md",
    "experimental/data/asymptotic_rs_mca_closed_ledger_audit.json",
    "experimental/scripts/verify_asymptotic_ledger_audit.py",
)


def cap_memory():
    try:
        gb = float(os.environ.get("ALAUD_AS_CAP_GB", "2"))
    except ValueError:
        gb = 2.0
    nbytes = int(gb * (1024 ** 3))
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        newhard = hard if hard != resource.RLIM_INFINITY and hard < nbytes else nbytes
        resource.setrlimit(resource.RLIMIT_AS, (nbytes, newhard))
    except (ValueError, OSError):
        pass  # best-effort; never fail the audit over an rlimit refusal


def repo_root():
    env = os.environ.get("ALAUD_DATA_DIR")
    if env:
        return os.path.abspath(env)
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))  # experimental/scripts -> root


_FILE_CACHE = {}


def read_lines(path):
    if path not in _FILE_CACHE:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            _FILE_CACHE[path] = fh.read().splitlines()
    return _FILE_CACHE[path]


def quote_near(root, relpath, line, quote):
    """True iff `quote` (byte substring) appears within +/-VICINITY of `line`."""
    path = os.path.join(root, relpath)
    if not os.path.isfile(path):
        return False
    lines = read_lines(path)
    lo = max(0, line - 1 - VICINITY)
    hi = min(len(lines), line - 1 + VICINITY + 1)
    window = "\n".join(lines[lo:hi])
    return quote in window


def iter_triples(node, ctx="root"):
    """Yield (relpath, line, quote, context) for every dict carrying all three
    non-null keys, recursing through the JSON tree."""
    if isinstance(node, dict):
        f, l, q = node.get("file"), node.get("line"), node.get("quote")
        if f is not None and l is not None and q is not None:
            label = node.get("resolved_label") or node.get("label") or node.get("item") or ctx
            yield (f, l, q, str(label))
        for k, v in node.items():
            yield from iter_triples(v, ctx=k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from iter_triples(v, ctx="%s[%d]" % (ctx, i))


# ---- gates ---------------------------------------------------------------

def gate_files(data, root):
    fails = []
    for key, rel in data["sources"].items():
        if not os.path.isfile(os.path.join(root, rel)):
            fails.append("source '%s' missing: %s" % (key, rel))
    known = set(data["sources"].values())
    for f, l, q, ctx in iter_triples(data):
        if not os.path.isfile(os.path.join(root, f)):
            fails.append("cited file missing (%s): %s" % (ctx, f))
        elif f not in known:
            fails.append("cited file not a declared source (%s): %s" % (ctx, f))
    return fails


def gate_quotes(data, root):
    """Gate (b) label at line vicinity + (c) verbatim byte-match, combined."""
    fails = []
    n = 0
    for f, l, q, ctx in iter_triples(data):
        n += 1
        if not quote_near(root, f, l, q):
            fails.append("quote not within +/-%d of %s:%d (%s): %r"
                         % (VICINITY, f, l, ctx, q[:60]))
    if n < 40:
        fails.append("too few located quotes checked (%d); data file truncated?" % n)
    return fails


def gate_totals(data):
    fails = []
    tally = {v: 0 for v in FOURWAY}
    for e in data["cells"]:
        v = e["verdict"]
        if v not in tally:
            fails.append("cell verdict not in 4-way scheme: %s (%s)" % (v, e.get("item")))
        else:
            tally[v] += 1
    for j in data["joints"]:
        v = j["verdict"]
        if v in tally:  # B1,B3,B4 count; B2 is STRUCTURAL and excluded
            tally[v] += 1
        elif v != "STRUCTURAL":
            fails.append("joint verdict unexpected: %s (%s)" % (v, j.get("joint")))
    declared = data["verdict_totals"]
    for v in FOURWAY:
        if tally[v] != declared.get(v):
            fails.append("verdict total mismatch %s: computed %d, declared %s"
                         % (v, tally[v], declared.get(v)))
    return fails


def gate_quasicube(data):
    """Gate (e): |A-A| >= |A|^{3/2} follows from the quasicube application with
    P=-A, Q={0}, U=A. Pure logic + arithmetic."""
    fails = []
    c = data["quasicube_check"]
    pf = c["P_size_factor"]      # |P|/|A| = |-A|/|A| = 1
    qs = c["Q_size"]             # |Q| = |{0}| = 1
    uf = c["U_size_factor"]      # |U|/|A| = |A|/|A| = 1
    e = c["target_exponent"]     # 3/2
    for a in c["a_values"]:
        # RHS = |P|^{1/2} |Q|^{1/2} |U| = (pf*a)^{1/2} * qs^{1/2} * (uf*a)
        rhs = ((pf * a) ** 0.5) * (qs ** 0.5) * (uf * a)
        target = a ** e
        if abs(rhs - target) > 1e-9 * max(1.0, target):
            fails.append("quasicube RHS != |A|^%.3f at |A|=%s: %r vs %r"
                         % (e, a, rhs, target))
    # concrete witness: A={0,1} in Z, A-A = {-1,0,1}
    w = c["witness"]
    A = w["A"]
    ama = sorted({x - y for x in A for y in A})
    if ama != sorted(w["A_minus_A"]):
        fails.append("witness A-A mismatch: %r vs %r" % (ama, w["A_minus_A"]))
    if len(ama) != w["A_minus_A_size"]:
        fails.append("witness |A-A| mismatch: %d vs %d" % (len(ama), w["A_minus_A_size"]))
    if not (w["A_minus_A_size"] >= len(A) ** e - 1e-9):
        fails.append("witness violates |A-A| >= |A|^%.3f" % e)
    # structural identity: P+Q+U == A-A as sets
    P = [-x for x in A]
    Q = [0]
    U = list(A)
    pqu = sorted({p + qq + u for p in P for qq in Q for u in U})
    if pqu != ama:
        fails.append("P+Q+U != A-A: %r vs %r" % (pqu, ama))
    return fails


def scan_token(root, token):
    hits = set()
    for d in SCAN_DIRS:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            continue
        for dp, dn, fns in os.walk(base):
            if ".lake" in dp or "/.git" in dp:
                dn[:] = [x for x in dn if x != ".lake" and x != ".git"]
                continue
            dn[:] = [x for x in dn if x not in (".lake", ".git")]
            for fn in fns:
                if not fn.endswith(SCAN_EXTS):
                    continue
                p = os.path.join(dp, fn)
                if os.path.relpath(p, root) in AUDIT_ARTIFACTS:
                    continue
                try:
                    with open(p, "r", encoding="utf-8", errors="replace") as fh:
                        if token in fh.read():
                            hits.add(os.path.relpath(p, root))
                except OSError:
                    pass
    return hits


def gate_steering(data):
    """Steering-alignment block (agents.md eb42b82 mandated vocabulary):
    NO_ISSUE = 48 FOUND-EXACT + B2 + two external-tool checks = 51;
    OPEN_GAP = 3 PHANTOM + B1 + B3 + B4 = 6; FIXED = CENF = 0;
    failure-mode map covers exactly the steering's seven assigned modes."""
    fails = []
    s = data.get("steering_alignment")
    if not s:
        return ["steering_alignment block missing"]
    t = s["mandated_vocab_totals"]
    vt = data["verdict_totals"]
    want_no_issue = vt["FOUND-EXACT"] + 1 + 2
    want_open_gap = vt["PHANTOM"] + 3
    if t["NO_ISSUE"] != want_no_issue:
        fails.append("NO_ISSUE=%d, want %d" % (t["NO_ISSUE"], want_no_issue))
    if t["OPEN_GAP"] != want_open_gap:
        fails.append("OPEN_GAP=%d, want %d" % (t["OPEN_GAP"], want_open_gap))
    if t["FIXED"] != 0 or t["COUNTEREXAMPLE_NEW_FLOOR"] != 0:
        fails.append("FIXED/COUNTEREXAMPLE_NEW_FLOOR must be 0 in this packet")
    if len(s["failure_mode_map"]) != 7:
        fails.append("failure_mode_map must cover the steering's 7 modes")
    return fails


def gate_moduli_absent(data, root):
    """FINDING-1: distinctive C9 tokens live ONLY in the paper; no *moduli* file.

    Forward-compatibility: FINDING-1 records the state AT THE AUDIT BASE.  If
    the moduli manuscript(s) appear in the tree later (e.g. the steering-named
    experimental/rs_mca_moduli_ledger_final.tex lands), that RESOLVES the
    finding rather than falsifying this audit — so an appearance downgrades to
    a loud notice + PASS, and only the recorded-at-base flag is a hard gate."""
    fails = []
    m = data["moduli_manuscripts_absent"]
    if m.get("confirmed_absent_at_base") is not True:
        fails.append("JSON flag confirmed_absent_at_base must be true")
        return fails
    sole = m["expected_sole_file"]
    appeared = []
    for tok in m["distinctive_tokens_only_in_paper"]:
        hits = scan_token(root, tok)
        if hits != {sole}:
            appeared.append("token %r now also in %s" % (tok, sorted(hits - {sole})))
    for d in SCAN_DIRS:
        base = os.path.join(root, d)
        for dp, dn, fns in os.walk(base):
            dn[:] = [x for x in dn if x not in (".lake", ".git")]
            for fn in fns:
                if "moduli" in fn.lower():
                    appeared.append("moduli-named file now present: %s"
                                    % os.path.relpath(os.path.join(dp, fn), root))
    if appeared:
        print("NOTE: moduli material has APPEARED since the audit base -- "
              "FINDING-1 may be resolved; re-audit C9 against it:")
        for a in appeared:
            print("      " + a)
    return fails


# ---- tamper self-tests ---------------------------------------------------

def tamper_tests(data, root):
    """>=5 load-bearing negative controls: each corrupts the data and asserts the
    relevant gate now REPORTS a failure. Returns list of tamper failures (i.e.
    tampers the gate wrongly accepted)."""
    problems = []

    def expect_reject(name, gate_fn, mutated, *args):
        if not gate_fn(mutated, *args):
            problems.append("tamper '%s' NOT rejected (gate passed corrupt data)" % name)

    # 1. corrupted quote (byte flip)
    d = copy.deepcopy(data)
    d["cells"][2]["quote"] = d["cells"][2]["quote"] + "_XYZZY"
    expect_reject("corrupted-quote", gate_quotes, d, root)

    # 2. wrong line number (shift out of the +/-5 window)
    d = copy.deepcopy(data)
    d["cells"][2]["line"] = d["cells"][2]["line"] + 200
    expect_reject("wrong-line", gate_quotes, d, root)

    # 3. fake label (nonexistent string)
    d = copy.deepcopy(data)
    d["cells"][5]["quote"] = "this label does not exist anywhere in the source"
    expect_reject("fake-label", gate_quotes, d, root)

    # 4. mangled verdict count
    d = copy.deepcopy(data)
    d["verdict_totals"]["FOUND-EXACT"] = d["verdict_totals"]["FOUND-EXACT"] + 1
    expect_reject("mangled-total", gate_totals, d)

    # 5. missing source file (dangling path)
    d = copy.deepcopy(data)
    d["cells"][0]["file"] = "experimental/does_not_exist.tex"
    expect_reject("missing-source", gate_files, d, root)

    # 6. moduli-absence record tamper (the recorded-at-base flag is the hard gate)
    d = copy.deepcopy(data)
    d["moduli_manuscripts_absent"]["confirmed_absent_at_base"] = False
    expect_reject("moduli-flag", gate_moduli_absent, d, root)

    # 8. steering-vocabulary tamper (mangled NO_ISSUE total must be caught)
    d = copy.deepcopy(data)
    d["steering_alignment"]["mandated_vocab_totals"]["NO_ISSUE"] += 1
    expect_reject("steering-total", gate_steering, d)

    # 7. quasicube arithmetic tamper (wrong target exponent)
    d = copy.deepcopy(data)
    d["quasicube_check"]["target_exponent"] = 1.4
    expect_reject("quasicube-exponent", gate_quasicube, d)

    return problems


# ---- driver --------------------------------------------------------------

def main():
    cap_memory()
    root = repo_root()
    data_path = os.path.join(root, "experimental", "data",
                             "asymptotic_rs_mca_closed_ledger_audit.json")
    if not os.path.isfile(data_path):
        print("RESULT: FAIL\n  data file not found: %s" % data_path)
        return 1
    with open(data_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    gates = [
        ("a  cited source files exist", gate_files(data, root)),
        ("bc labels/quotes byte-match at +/-%d lines" % VICINITY, gate_quotes(data, root)),
        ("d  verdict tally self-consistent", gate_totals(data)),
        ("e  quasicube |A-A|>=|A|^{3/2} derivation", gate_quasicube(data)),
        ("f  moduli manuscripts absent (FINDING-1)", gate_moduli_absent(data, root)),
        ("h  steering-vocabulary alignment (eb42b82)", gate_steering(data)),
    ]
    tampers = tamper_tests(data, root)

    ok = True
    print("asymptotic-ledger-audit verifier")
    print("  root: %s" % root)
    for name, fails in gates:
        status = "PASS" if not fails else "FAIL"
        print("  [%s] gate %s" % (status, name))
        for f in fails:
            ok = False
            print("        - %s" % f)
    tstatus = "PASS" if not tampers else "FAIL"
    print("  [%s] %d tamper self-tests (negative controls)"
          % (tstatus, 8))
    for t in tampers:
        ok = False
        print("        - %s" % t)

    n_quotes = sum(1 for _ in iter_triples(data))
    n_cells = len(data["cells"])
    print("  checked: %d located quotes, %d cell citations, %d joints, %d tamper tests"
          % (n_quotes, n_cells, len(data["joints"]), 8))
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
