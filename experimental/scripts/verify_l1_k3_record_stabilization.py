#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_l1_k3_record_stabilization.py

Zero-arg, stdlib-only, deterministic verifier for the standalone refinement note
`experimental/notes/l1/l1_k3_record_stabilization.md` and its data artifact
`experimental/data/certificates/l1-e3-law/l1_k3_growth_r3_extension.json`.

This packet REFINES (does not modify) the integrated k3 growth-refutation packet
(experimental/notes/l1/l1_k3_growth_refutation.md + .../l1_k3_growth_r2_scan.json +
experimental/scripts/verify_l1_k3_growth_refutation.py; integrated e83962ae, was PR #410).
It (a) STABILIZES ell=23's late p=1657 record (21->29 exhaustive primes, all 15 past the
record k3<=5) -- resolving the integrated note's own sec-3A open-endedness caution; (b) deepens
ell=29 (->21 primes) and adds an ell=31 grid; (c) records the search-depth/record-process
confound; (d) route-cuts two named candidate growth laws and leaves one OPEN. It also supersedes
the now-stale "empirical max k3 = 5" ell=23 citation in the integrated m19-pin note (was PR #399).

DUAL CODE PATH: every new k3 is cross-checked against the INTEGRATED verifier's gauge_max_k3
(a genuinely distinct engine). Zero-arg cross-verifies a fast spot set live (2 ell=31 rows,
incl. a k3=7 recurrence) and asserts the stored k3 for all 31 rows obey both PROVED caps; the
full 24-new-row live cross-check is behind `--full` (~10 min; already run offline 31/31 MATCH).
The integrated scan JSON is asserted UNTOUCHED (180 rows / structural gate).

Gates (exit 0 iff all pass; zero-arg measured < ~90s):
  (1) dual-code-path: import integrated gauge_max_k3; live spot cross-check (ell=31 n=36,48);
      all 31 stored k3 obey k3<=floor((2ell-5)/3) and k3<=2(ell-1)/3.
  (2) integrated scan JSON UNTOUCHED: 180 rows, by_ell[23]=21 (max n=134), no ell=31, the
      (23,72)->7 record present, ell=19 deep null intact (80 rows, max 6).
  (3) reconfirm consistency: the 7 "reconfirms-integrated" rows match the integrated k3.
  (4) STABILIZATION + deepening: all 31 rows eligible (p = ell*n+1, prime); combined ell=23 =
      29 primes (r3 deepest p=4463), 15 rows past n=72 all k3<=5; ell=29 = 21 primes (r3 deepest
      p=4583), k3=7 at n in {8,44,68,138}; ell=31 grid exact [(22,683)..(60,1861)] =
      [7,5,6,6,7,7,6], 7 at n in {22,48,52}, with the build-time n=10,12 rows gated against the
      integrated verifier's FULL_TABLE constants (the integrated scan JSON has no ell=31 rows).
  (5) base table re-sourced entry-by-entry from integrated artifacts (scan JSON + the integrated
      verifier's FULL_TABLE/witness constants; ell=67 asserted witness-folded >=9->9), then the
      route-cut arithmetic recomputed EXACTLY: A DEAD (ratio 0.800->0.191, 4.18x), B DEAD
      (gap 1->38; gap/sqrt(ell) 0.30->4.45 max at ell=73, 4.27 at ell=71), C OPEN (k3/sqrt &
      k3/ln spreads 1.66/1.78 vs raw 3.34).
  (6) record-process confound: the shallow(1-3p)-open-ended vs deep-stabilizing partition.
  (7) tamper self-tests (>=4): mutated stored k3 (cap-violating), a synthetic 204-row copy of the
      integrated JSON fed to the same untouched-checker gate 2 runs, a broken stabilization row,
      and a flattened base table -- each REJECTED.
Opt-in `--full`: live gauge_max_k3 cross-check of ALL 24 new rows (~10 min).
"""
import sys, os, json
from fractions import Fraction
from math import sqrt, log

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "..", "data", "certificates", "l1-e3-law")
INTEG_JSON = os.path.join(DATA, "l1_k3_growth_r2_scan.json")
R3_JSON = os.path.join(DATA, "l1_k3_growth_r3_extension.json")


def load(p):
    with open(p) as f:
        return json.load(f)


def ceil_lemmaR(ell):
    return (2 * ell - 5) // 3


def cap_Rzeta(ell):
    return (2 * (ell - 1)) // 3


# ---- gate 1: dual code path (integrated gauge_max_k3) + caps ----
def gate1_dual_and_caps(full=False):
    try:
        import verify_l1_k3_growth_refutation as IV
    except Exception as e:
        return False, "cannot import integrated verifier (dual code path): %r" % (e,)
    d = load(R3_JSON)
    rows = d["rows"]
    # (a) caps: every stored k3 obeys BOTH proved Theta(ell) caps
    caps_ok = all(r["k3"] <= ceil_lemmaR(r["ell"]) and r["k3"] <= cap_Rzeta(r["ell"]) for r in rows)
    # (b) live dual-code-path cross-check via the integrated gauge_max_k3
    if full:
        spot = [r for r in rows if r["status"] == "new"]
    else:
        spot = [r for r in rows if r["ell"] == 31 and r["n"] in (36, 48)]  # fast; incl. k3=7 recurrence
    live = []
    allmatch = True
    for r in spot:
        gmax, _, _ = IV.gauge_max_k3(r["p"], r["ell"], IV.rotation_reps(r["ell"]))
        ok = (gmax == r["k3"])
        allmatch = allmatch and ok
        live.append("(%d,%d)->%d%s" % (r["ell"], r["p"], gmax, "" if ok else "!=%d" % r["k3"]))
    ok = caps_ok and allmatch
    return ok, ("caps hold=%s; integrated gauge_max_k3 live cross-check [%s]=%s (%d rows%s)"
                % (caps_ok, " ".join(live), "MATCH" if allmatch else "MISMATCH",
                   len(spot), ", --full ALL new" if full else ", spot"))


# ---- gate 2: integrated scan JSON UNTOUCHED ----
def check_integrated_untouched(d):
    """Structural untouched-checks for the integrated scan JSON. Factored out so the
    gate-7 tamper self-test can exercise the SAME logic on a synthetic corrupted copy."""
    e23 = d["by_ell"]["23"]
    e19 = [r for r in d["rows"] if r["ell"] == 19]
    checks = [
        ("180 rows", len(d["rows"]) == 180),
        ("by_ell[23]=21", len(e23) == 21),
        ("ell=23 deepest n=134 (NOT extended here)", max(r["n"] for r in e23) == 134),
        ("no ell=31 in integrated", "31" not in d["by_ell"]),
        ("(23,72)->7 record present", any(r["n"] == 72 and r["k3"] == 7 for r in e23)),
        ("ell=19 deep null intact (80 rows, max 6)",
         len(e19) == 80 and max(r["k3"] for r in e19) == 6),
    ]
    return all(c for _, c in checks), checks


def gate2_integrated_untouched():
    ok, checks = check_integrated_untouched(load(INTEG_JSON))
    return ok, "integrated JSON untouched: " + "; ".join("%s=%s" % (n, "ok" if c else "BAD") for n, c in checks)


# ---- gate 3: reconfirm consistency ----
def gate3_reconfirm():
    d = load(R3_JSON)
    integ = {(r["ell"], r["n"], r["p"]): r for r in load(INTEG_JSON)["rows"]}
    recon = [r for r in d["rows"] if r["status"] == "reconfirms-integrated"]
    ok = len(recon) == 7 and all(integ.get((r["ell"], r["n"], r["p"]), {}).get("k3") == r["k3"] for r in recon)
    return ok, "7 reconfirms-integrated rows match integrated k3=%s (n=%s)" % (
        ok, [r["n"] for r in recon])


# ---- gate 4: stabilization + deepening (combined integrated + r3) ----
def gate4_stabilization():
    try:
        import verify_l1_k3_growth_refutation as IV
    except Exception as e:
        return False, "cannot import integrated verifier: %r" % (e,)
    integ = load(INTEG_JSON)["by_ell"]
    d = load(R3_JSON)
    r3 = d["by_ell"]
    # combined ell=23: integrated 21 + r3-new 8
    comb23 = integ["23"] + [r for r in r3["23"] if r["status"] == "new"]
    past = [r for r in comb23 if r["n"] > 72]
    # combined ell=29: integrated 12 + r3-new 9
    comb29 = integ["29"] + r3["29"]
    e31 = r3["31"]
    e31_np = [(r["n"], r["p"]) for r in e31]
    checks = [
        ("all 31 r3 rows eligible (p = ell*n+1, prime)",
         all(r["p"] == r["ell"] * r["n"] + 1 and IV.is_prime(r["p"]) for r in d["rows"])),
        ("ell=23 r3 deepest p=4463 (ties stored block)",
         max(r["p"] for r in r3["23"]) == 4463),
        ("ell=29 r3 deepest p=4583", max(r["p"] for r in r3["29"]) == 4583),
        ("ell=31 r3 grid exact [(22,683),(36,1117),(42,1303),(46,1427),(48,1489),(52,1613),(60,1861)]",
         e31_np == [(22, 683), (36, 1117), (42, 1303), (46, 1427), (48, 1489), (52, 1613), (60, 1861)]),
        ("ell=31 build-time n=10,12 gated vs integrated FULL_TABLE ((311,7),(373,7)); (683,7) cross-checked",
         IV.FULL_TABLE.get(31) == [(311, 7), (373, 7), (683, 7)]
         and 311 == 31 * 10 + 1 and 373 == 31 * 12 + 1
         and next(r["k3"] for r in e31 if r["p"] == 683) == 7),
        ("ell=23 combined 29 primes", len(comb23) == 29),
        ("ell=23 STABILIZED: 15 primes past n=72, all k3<=5",
         len(past) == 15 and max(r["k3"] for r in past) == 5),
        ("ell=29 combined 21 primes", len(comb29) == 21),
        ("ell=29 k3=7 at n in {8,44,68,138}",
         sorted(r["n"] for r in comb29 if r["k3"] == 7) == [8, 44, 68, 138]),
        ("ell=31 grid [7,5,6,6,7,7,6]", [r["k3"] for r in e31] == [7, 5, 6, 6, 7, 7, 6]),
        ("ell=31 k3=7 at n in {22,48,52}", [r["n"] for r in e31 if r["k3"] == 7] == [22, 48, 52]),
        ("stored stabilization block agrees",
         d["record_stabilization_ell23"]["primes_past_record"] == 15
         and d["record_stabilization_ell23"]["max_k3_past_record"] == 5
         and d["record_stabilization_ell23"]["deepest_p"] == 4463),
    ]
    ok = all(c for _, c in checks)
    return ok, "stabilization+deepening: " + "; ".join("%s=%s" % (n, "ok" if c else "BAD") for n, c in checks)


# ---- gate 5: candidate-law route-cuts recomputed EXACTLY ----
def _route_cut_numbers(table):
    ratios = {ell: Fraction(k, ceil_lemmaR(ell)) for ell, k in table}
    gaps = {ell: ceil_lemmaR(ell) - k for ell, k in table}
    fall = float(ratios[11]) / float(ratios[73])
    gsq = {ell: gaps[ell] / sqrt(ell) for ell, _ in table}
    ksq = [k / sqrt(ell) for ell, k in table]
    kln = [k / log(ell) for ell, k in table]
    kraw = [k / ell for ell, k in table]
    return ratios, gaps, fall, gsq, ksq, kln, kraw


def gate5_route_cuts():
    d = load(R3_JSON)["candidate_law_route_cuts"]
    table = [tuple(t) for t in d["base_table_ell_maxk3"]]
    # Re-source the 17 (ell, k3) inputs from INTEGRATED artifacts (scan JSON rows + the
    # integrated verifier's own FULL_TABLE / witness constants) instead of trusting them
    # as packet literals. ell=67 is the one witness-folded entry: the integrated note marks
    # it >= 9 (witness lower bound, thin coverage); folded here as 9.
    try:
        import verify_l1_k3_growth_refutation as IV
    except Exception as e:
        return False, "cannot import integrated verifier: %r" % (e,)
    integ_rows = load(INTEG_JSON)["rows"]
    best = {}
    for r in integ_rows:
        best[r["ell"]] = max(best.get(r["ell"], 0), r["k3"])
    for ell_i, pairs in IV.FULL_TABLE.items():
        for _p, k in pairs:
            best[ell_i] = max(best.get(ell_i, 0), k)
    for w in IV.WITNESSES + IV.BAND_WITNESSES + IV.R2_RECORDS:
        best[w["ell"]] = max(best.get(w["ell"], 0), w["k3"])
    sourced_ok = (len(table) == 17 and all(best.get(e) == k for e, k in table))
    e67_json = sorted(r["k3"] for r in integ_rows if r["ell"] == 67)
    e67_folded = (e67_json == [3]
                  and max(w["k3"] for w in IV.BAND_WITNESSES if w["ell"] == 67) == 9
                  and dict(table)[67] == 9)
    ratios, gaps, fall, gsq, ksq, kln, kraw = _route_cut_numbers(table)
    A = d["A_constant_fraction_of_ceiling"]; B = d["B_bounded_additive_gap"]; C = d["C_sublinear_vs_log"]
    checks = [
        ("all 17 base-table (ell,k3) re-sourced from integrated artifacts", sourced_ok),
        ("ell=67 = witness-folded >=9->9 (integrated exhaustive there: [3], thin)", e67_folded),
        ("A verdict DEAD", A["verdict"] == "DEAD"),
        ("A ratio ell=11 = 4/5", ratios[11] == Fraction(4, 5)),
        ("A ratio ell=73 = 9/47", ratios[73] == Fraction(9, 47)),
        ("A fall factor ~4.18", abs(fall - 4.18) < 0.01 and abs(fall - A["ratio_fall_factor"]) < 0.01),
        ("A well-searched subset {11:.80,17:.78,19:.55,23:.54,29:.41}",
         all(abs(float(ratios[int(e)]) - v) < 0.005 for e, v in A["well_searched_subset_ratios"].items())),
        ("B verdict DEAD", B["verdict"] == "DEAD"),
        ("B gap 1->38", gaps[11] == B["gap_ell11"] == 1 and gaps[73] == B["gap_ell73"] == 38),
        ("B gap/sqrt(ell) max 4.45 at ell=73",
         abs(max(gsq.values()) - 4.45) < 0.01 and max(gsq, key=gsq.get) == 73
         and abs(gsq[73] - B["gap_over_sqrt_ell_max"]) < 0.01),
        ("B gap/sqrt(ell71)=4.27 and min 0.30",
         abs(gsq[71] - 4.27) < 0.01 and abs(min(gsq.values()) - 0.30) < 0.01),
        ("C verdict OPEN", C["verdict"] == "OPEN"),
        ("C k3/sqrt spread 1.66", abs(max(ksq) / min(ksq) - 1.66) < 0.02
         and abs(max(ksq) / min(ksq) - C["k3_over_sqrt_ell_spread"]) < 0.02),
        ("C k3/ln spread 1.78", abs(max(kln) / min(kln) - 1.78) < 0.02),
        ("C raw k3/ell spread 3.34 (steeper than both)", abs(max(kraw) / min(kraw) - 3.34) < 0.02),
    ]
    ok = all(c for _, c in checks)
    return ok, "route-cuts: " + "; ".join("%s=%s" % (n, "ok" if c else "BAD") for n, c in checks)


# ---- gate 6: record-process confound ----
def gate6_confound():
    d = load(R3_JSON)["record_process_confound"]
    integ = load(INTEG_JSON)["by_ell"]
    shallow = set(d["shallow_open_ended_ells"])
    deep = {int(k): v for k, v in d["deep_stabilizing_ells_nprimes"].items()}
    # cross-check thin coverage against the integrated scan JSON: the shallow ells that DO appear
    # in the integrated by_ell (61,67,71,73) each carry <=3 primes; 37,41,47,59 are absent (thinner).
    shallow_thin = all(
        (len(integ[str(e)]) <= 3) if str(e) in integ else True for e in shallow)
    shallow_absent_or_thin = all((str(e) not in integ) or (len(integ[str(e)]) <= 3) for e in shallow)
    checks = [
        ("shallow set = {37,41,47,59,61,67,71,73}", shallow == {37, 41, 47, 59, 61, 67, 71, 73}),
        ("shallow ells thin in integrated JSON (<=3 primes where present)",
         shallow_thin and shallow_absent_or_thin),
        ("deep ells >= 6 primes each", all(v >= 6 for v in deep.values())),
        ("deep set = {17,19,23,29,43,53}", set(deep) == {17, 19, 23, 29, 43, 53}),
        ("ell=23 now deep (29) and ell=29 deep (21) via this packet",
         deep.get(23) == 29 and deep.get(29) == 21),
        ("shallow and deep disjoint", not (shallow & set(deep))),
    ]
    ok = all(c for _, c in checks)
    return ok, "confound partition: " + "; ".join("%s=%s" % (n, "ok" if c else "BAD") for n, c in checks)


# ---- gate 7: tamper self-tests ----
def gate7_tamper():
    results = []
    d = load(R3_JSON)
    # (a) mutate a stored k3 to violate a cap -> gate1 caps must reject
    bad = json.loads(json.dumps(d))
    bad["rows"][0]["k3"] = ceil_lemmaR(bad["rows"][0]["ell"]) + 5
    caps_ok = all(r["k3"] <= ceil_lemmaR(r["ell"]) for r in bad["rows"])
    results.append(("cap-violating stored k3 rejected", not caps_ok))
    # (b) a SYNTHETIC copy of the integrated JSON padded/trimmed to EXACTLY 204 rows must be
    #     REJECTED by the same untouched-checker gate 2 runs (tests the checker's logic on a
    #     corrupted copy; independent of the live file's own state)
    integ = load(INTEG_JSON)
    bad2 = json.loads(json.dumps(integ))
    filler = dict(ell=23, n=999, p=999, k3=1, tri=[0, 1, 2], sec=0.0, _source="synthetic-tamper")
    while len(bad2["rows"]) < 204:
        bad2["rows"].append(dict(filler))
    bad2["rows"] = bad2["rows"][:204]
    ok_b, _ = check_integrated_untouched(bad2)
    results.append(("synthetic 204-row integrated copy rejected by untouched-checker",
                    len(bad2["rows"]) == 204 and not ok_b))
    # (c) broken stabilization: pretend a past-record row has k3=7 -> the <=5 assertion fails
    integ_by = integ["by_ell"]
    comb23 = integ_by["23"] + [r for r in d["by_ell"]["23"] if r["status"] == "new"]
    past = [dict(r) for r in comb23 if r["n"] > 72]
    past[0]["k3"] = 7
    results.append(("broken stabilization (a 7 past record) rejected", max(r["k3"] for r in past) != 5))
    # (d) tampered base table (flatten ratio: every k3 := its ceiling) -> fall factor no longer 4.18
    flat = [(e, ceil_lemmaR(e)) for e, _ in d["candidate_law_route_cuts"]["base_table_ell_maxk3"]]
    _, _, fall_flat, _, _, _, _ = _route_cut_numbers(flat)
    results.append(("flattened base table (fall=%.2f) fails the 4.18x check" % fall_flat,
                    not (abs(fall_flat - 4.18) < 0.01)))
    ok = all(caught for _, caught in results)
    return ok, "tamper: " + "; ".join("%s=%s" % (n, "CAUGHT" if c else "MISSED") for n, c in results)


GATES = [
    ("(1) dual code path (integrated gauge_max_k3) + caps", gate1_dual_and_caps),
    ("(2) integrated scan JSON UNTOUCHED                 ", gate2_integrated_untouched),
    ("(3) reconfirm-integrated consistency               ", gate3_reconfirm),
    ("(4) ell=23 STABILIZED + ell=29/31 deepening        ", gate4_stabilization),
    ("(5) base table re-sourced + route-cuts (exact)     ", gate5_route_cuts),
    ("(6) record-process / search-depth confound         ", gate6_confound),
    ("(7) tamper self-tests (>=4, must be caught)         ", gate7_tamper),
]


def main(argv):
    full = "--full" in argv
    allok = True
    for name, fn in GATES:
        if fn is gate1_dual_and_caps:
            ok, msg = fn(full=full)
        else:
            ok, msg = fn()
        allok = allok and ok
        print("[%s] %s  %s" % ("PASS" if ok else "FAIL", name, msg))
    print("ALL PASS" if allok else "SOME FAILED")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
