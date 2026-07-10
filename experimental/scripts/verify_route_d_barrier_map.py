#!/usr/bin/env python3
"""Verifier for the CAP25 v13 Route-D shared barrier map.

Zero-arg, stdlib-only, deterministic. Gates the provenance-gated synthesis note
`experimental/notes/thresholds/cap25_v13_route_d_barrier_map.md` and its machine
map `experimental/data/cap25_v13_route_d_barrier_map.json` against the real
source files in the tree at base 84b393e.

Gates:
  (a) every cited source file exists at its stated path;
  (b) every verbatim quote (node evidence, proved-edge, dead-route) is an exact
      byte substring of its cited source file;
  (c) every numeric constant in the node ledger matches a regex-extracted
      numeric token of its source file;
  (d) the proved-edge graph is a DAG (no cycles);
  (e) node / proved-edge / speculative-edge / dead-route counts agree between the
      JSON, the JSON's own stated totals, and the note's machine-readable TOTALS
      line;
  (f) provenance fence: proved edges carry a real quote+source and are never
      labelled ANALYSIS-CONJECTURAL; speculative edges carry the
      ANALYSIS-CONJECTURAL label and no source_file/quote.

Plus >=5 load-bearing tamper self-tests (each mutates an in-memory copy and
asserts the relevant gate fails).

Knobs (environment):
  RDMAP_DATA_DIR   directory holding the JSON (default: <repo>/experimental/data)
  RDMAP_AS_CAP_GB  address-space soft cap in GiB applied at startup (default: 2)

Exit 0 = PASS. Target runtime < 30 s (actual: << 1 s).
"""
import os
import re
import sys
import json
import copy

# ---------------------------------------------------------------- environment
def _apply_as_cap():
    try:
        gb = float(os.environ.get("RDMAP_AS_CAP_GB", "2"))
    except ValueError:
        gb = 2.0
    if gb <= 0:
        return
    try:
        import resource
        cap = int(gb * (1024 ** 3))
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        newhard = hard if hard != resource.RLIM_INFINITY and hard < cap else cap
        if soft == resource.RLIM_INFINITY or soft > cap:
            resource.setrlimit(resource.RLIMIT_AS, (cap, newhard))
    except Exception:
        pass  # best-effort only; never block the verify on the cap

_apply_as_cap()

# this script lives at <repo>/experimental/scripts/ ; go up three to <repo>
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.environ.get("RDMAP_DATA_DIR", os.path.join(REPO_ROOT, "experimental", "data"))
JSON_PATH = os.path.join(DATA_DIR, "cap25_v13_route_d_barrier_map.json")
NOTE_PATH = os.path.join(REPO_ROOT, "experimental", "notes", "thresholds",
                         "cap25_v13_route_d_barrier_map.md")

NUM_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")

_src_cache = {}
def read_source(rel_path):
    """Read a repo-root-relative source file (cached)."""
    if rel_path not in _src_cache:
        full = os.path.join(REPO_ROOT, rel_path)
        with open(full, encoding="utf-8") as f:
            _src_cache[rel_path] = f.read()
    return _src_cache[rel_path]

def digits(s):
    return re.sub(r"[^0-9]", "", s)

def source_tokens(body):
    return {digits(m.group()) for m in NUM_RE.finditer(body) if digits(m.group())}


# ---------------------------------------------------------------- the gates
def gate_a_files_exist(data):
    """(a) every cited source file exists."""
    errs = []
    cited = set()
    for n in data["nodes"]:
        cited.add(n["source_file"])
    for e in data["proved_edges"]:
        cited.add(e["source_file"])
    for d in data["dead_routes"]:
        cited.add(d["killing_source"])
    for rel in sorted(cited):
        if not os.path.isfile(os.path.join(REPO_ROOT, rel)):
            errs.append("missing cited file: %s" % rel)
    return errs

def gate_b_quotes(data):
    """(b) every quote is an exact byte substring of its cited source."""
    errs = []
    for n in data["nodes"]:
        body = read_source(n["source_file"])
        if n["evidence_quote"] not in body:
            errs.append("node %s: evidence_quote not in %s" % (n["id"], n["source_file"]))
    for e in data["proved_edges"]:
        body = read_source(e["source_file"])
        if e["quote"] not in body:
            errs.append("edge %s: quote not in %s" % (e["id"], e["source_file"]))
    for d in data["dead_routes"]:
        body = read_source(d["killing_source"])
        if d["quote"] not in body:
            errs.append("dead-route %s: quote not in %s" % (d["id"], d["killing_source"]))
    return errs

def gate_c_constants(data):
    """(c) every node constant matches a regex-extracted numeric token of its source."""
    errs = []
    for n in data["nodes"]:
        body = read_source(n["source_file"])
        toks = source_tokens(body)
        for c in n["constants"]:
            d = digits(c)
            if not d:
                errs.append("node %s: non-numeric constant %r" % (n["id"], c))
            elif d not in toks:
                errs.append("node %s: constant %r (digits %s) not a source token of %s"
                            % (n["id"], c, d, n["source_file"]))
    return errs

def gate_d_dag(data):
    """(d) proved-edge graph is a DAG."""
    node_ids = {n["id"] for n in data["nodes"]}
    adj = {}
    for e in data["proved_edges"]:
        if e["from"] not in node_ids:
            return ["edge %s: unknown 'from' %s" % (e["id"], e["from"])]
        if e["to"] not in node_ids:
            return ["edge %s: unknown 'to' %s" % (e["id"], e["to"])]
        adj.setdefault(e["from"], []).append(e["to"])
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}
    def dfs(u):
        color[u] = GRAY
        for v in adj.get(u, []):
            cv = color.get(v, WHITE)
            if cv == GRAY:
                return True
            if cv == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False
    for u in node_ids:
        if color.get(u, WHITE) == WHITE and dfs(u):
            return ["proved-edge graph contains a cycle (through %s)" % u]
    return []

def _note_totals(note_text):
    m = re.search(
        r"TOTALS:\s*nodes=(\d+)\s+proved_edges=(\d+)\s+speculative_edges=(\d+)\s+dead_routes=(\d+)",
        note_text)
    if not m:
        return None
    return {"nodes": int(m.group(1)), "proved_edges": int(m.group(2)),
            "speculative_edges": int(m.group(3)), "dead_routes": int(m.group(4))}

def gate_e_counts(data, note_text):
    """(e) counts agree JSON-array == JSON-totals == note TOTALS line."""
    errs = []
    actual = {"nodes": len(data["nodes"]), "proved_edges": len(data["proved_edges"]),
              "speculative_edges": len(data["speculative_edges"]),
              "dead_routes": len(data["dead_routes"])}
    stated = data.get("totals", {})
    for k, v in actual.items():
        if stated.get(k) != v:
            errs.append("JSON totals[%s]=%r != actual %d" % (k, stated.get(k), v))
    nt = _note_totals(note_text)
    if nt is None:
        errs.append("note has no machine-readable TOTALS line")
    else:
        for k, v in actual.items():
            if nt.get(k) != v:
                errs.append("note TOTALS[%s]=%r != actual %d" % (k, nt.get(k), v))
    return errs

def gate_f_fence(data):
    """(f) proved / speculative provenance fence."""
    errs = []
    for e in data["proved_edges"]:
        if e.get("label") == "ANALYSIS-CONJECTURAL":
            errs.append("proved edge %s is labelled ANALYSIS-CONJECTURAL" % e.get("id"))
        if not e.get("quote") or not e.get("source_file"):
            errs.append("proved edge %s lacks quote/source_file" % e.get("id"))
    for s in data["speculative_edges"]:
        if s.get("label") != "ANALYSIS-CONJECTURAL":
            errs.append("speculative edge %s missing ANALYSIS-CONJECTURAL label" % s.get("id"))
        if s.get("source_file") or s.get("quote"):
            errs.append("speculative edge %s smuggles a source_file/quote" % s.get("id"))
    return errs


GATES = [
    ("a: cited files exist", lambda d, note: gate_a_files_exist(d)),
    ("b: quotes are exact substrings", lambda d, note: gate_b_quotes(d)),
    ("c: constants match source tokens", lambda d, note: gate_c_constants(d)),
    ("d: proved-edge graph is a DAG", lambda d, note: gate_d_dag(d)),
    ("e: counts agree (json/totals/note)", lambda d, note: gate_e_counts(d, note)),
    ("f: proved/speculative provenance fence", lambda d, note: gate_f_fence(d)),
]


# ---------------------------------------------------------------- tamper tests
def tamper_tests(data, note_text):
    """>=5 load-bearing tamper tests: each mutation must make the named gate FAIL."""
    results = []

    # 1. corrupted quote -> gate (b) must fail
    d1 = copy.deepcopy(data)
    d1["nodes"][0]["evidence_quote"] = d1["nodes"][0]["evidence_quote"] + " __TAMPER__"
    results.append(("corrupted quote fails (b)", bool(gate_b_quotes(d1))))

    # 2. wrong constant -> gate (c) must fail (use the big cross-lineage target_floor)
    d2 = copy.deepcopy(data)
    hit = False
    for n in d2["nodes"]:
        for i, c in enumerate(n["constants"]):
            if c == "274836936291722953":
                n["constants"][i] = "274836936291722954"
                hit = True
                break
        if hit:
            break
    results.append(("wrong constant fails (c)", hit and bool(gate_c_constants(d2))))

    # 3. injected cycle -> gate (d) must fail
    d3 = copy.deepcopy(data)
    e0 = d3["proved_edges"][0]
    d3["proved_edges"].append({"id": "TAMPER-CYCLE", "from": e0["to"], "to": e0["from"],
                               "type": "tamper", "source_file": e0["source_file"],
                               "source_tag": e0.get("source_tag", ""), "quote": e0["quote"]})
    results.append(("injected cycle fails (d)", bool(gate_d_dag(d3))))

    # 4. missing-file cite -> gate (a) must fail
    d4 = copy.deepcopy(data)
    d4["nodes"][0]["source_file"] = "experimental/notes/thresholds/__does_not_exist__.md"
    results.append(("missing-file cite fails (a)", bool(gate_a_files_exist(d4))))

    # 5. speculative edge injected into the proved ledger -> fence (f) must fail
    d5 = copy.deepcopy(data)
    spec = copy.deepcopy(d5["speculative_edges"][0])  # has label, no source/quote
    d5["proved_edges"].append(spec)
    results.append(("speculative edge in proved ledger fails (f)", bool(gate_f_fence(d5))))

    # 6. mangled totals -> gate (e) must fail
    d6 = copy.deepcopy(data)
    d6["totals"]["nodes"] = d6["totals"]["nodes"] + 1
    results.append(("mangled totals fails (e)", bool(gate_e_counts(d6, note_text))))

    return results


# ---------------------------------------------------------------- main
def main():
    if not os.path.isfile(JSON_PATH):
        print("FAIL: map JSON not found at %s" % JSON_PATH)
        return 1
    if not os.path.isfile(NOTE_PATH):
        print("FAIL: note not found at %s" % NOTE_PATH)
        return 1
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    with open(NOTE_PATH, encoding="utf-8") as f:
        note_text = f.read()

    print("Route-D shared barrier-map verifier")
    print("  repo root : %s" % REPO_ROOT)
    print("  json      : %s" % os.path.relpath(JSON_PATH, REPO_ROOT))
    print("  note      : %s" % os.path.relpath(NOTE_PATH, REPO_ROOT))
    print("  totals    : %s" % json.dumps(data.get("totals", {})))
    print()

    ok = True
    for label, fn in GATES:
        errs = fn(data, note_text)
        status = "PASS" if not errs else "FAIL"
        print("  gate %-40s %s" % (label, status))
        for e in errs[:8]:
            print("       - %s" % e)
        if errs:
            ok = False

    print()
    print("  tamper self-tests (each mutation must FAIL its gate):")
    tamper_ok = True
    for label, failed in tamper_tests(data, note_text):
        status = "PASS" if failed else "FAIL(did not detect)"
        print("    %-52s %s" % (label, status))
        if not failed:
            tamper_ok = False

    print()
    if ok and tamper_ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
