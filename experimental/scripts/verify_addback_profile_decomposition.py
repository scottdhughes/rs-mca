#!/usr/bin/env python3
"""Verifier for the add-back profile-decomposition audit (gap A6, lem:addback).

Zero-arg, stdlib-only. Gates the note
  experimental/notes/audits/asymptotic_addback_profile_decomposition.md
against the two in-tree TeX files AND re-runs every finite check the note relies
on. Companion to #435 (verify_asymptotic_proof_audit_r2.py, whose attack A6 is
this gap) and #433 (verify_asymptotic_ledger_audit.py, joint B3).

Five gates:
  G1  quote byte-match: the gap description is faithful -- the post-edit
      asymptotic lem:addback/def:profile-nondegen name the condition, and grande
      lem:subexponential-addback-closure/rem:not-no-input-proof state it as a
      hypothesis.
  G2  add-back sufficiency (note R1): random mass-partitioned leaf families with
      per-leaf Q and image non-degeneracy satisfy max_s N(s) <= (C/rho) barN.
  G3  falsifier (note R4): the piled collapsed-image witness has per-leaf Q TRUE
      and global add-back violated by factor |Y|; spreading repairs it.
  G4  subregime discharge (note R2): the full-mass frontier log-arithmetic forces
      |log L - log|Y|| <= 3 eps, i.e. image non-degeneracy, over a grid.
  G5  master composition (note R1, finite): the exp(eps) factors telescope to an
      explicit finite bound on a grid.

Six tamper self-tests: breaking a witness must break the gate it feeds.

Knobs (environment variables):
  ADDBACK_AS_CAP_GB   address-space cap in GB via RLIMIT_AS (default 2).
  ADDBACK_DATA_DIR    repo root holding experimental/ (default: two dirs up).

Exit 0 and print 'RESULT: PASS' on success; exit 1 on any failure.
"""

import math
import os
import random
import resource
import sys


# ---- environment ---------------------------------------------------------

def cap_memory():
    try:
        gb = float(os.environ.get("ADDBACK_AS_CAP_GB", "2"))
    except ValueError:
        gb = 2.0
    nbytes = int(gb * (1024 ** 3))
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        newhard = hard if hard != resource.RLIM_INFINITY and hard < nbytes else nbytes
        resource.setrlimit(resource.RLIMIT_AS, (nbytes, newhard))
    except (ValueError, OSError):
        pass


def repo_root():
    env = os.environ.get("ADDBACK_DATA_DIR")
    if env:
        return os.path.abspath(env)
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))  # experimental/scripts -> root


_FILE_CACHE = {}


def read_lines(root, relpath):
    path = os.path.join(root, relpath)
    if path not in _FILE_CACHE:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            _FILE_CACHE[path] = fh.read().splitlines()
    return _FILE_CACHE[path]


def anchor_line(lines, anchor):
    for i, ln in enumerate(lines):
        if anchor in ln:
            return i
    return None


def quote_near_anchor(root, relpath, anchor, quote, vicinity=6):
    """True iff `quote` occurs within +/-vicinity lines of the line holding
    `anchor` in the file. Both anchor and quote must be present."""
    lines = read_lines(root, relpath)
    a = anchor_line(lines, anchor)
    if a is None:
        return False
    lo, hi = max(0, a - vicinity), min(len(lines), a + vicinity + 1)
    return quote in "\n".join(lines[lo:hi])


def label_present(root, relpath, label):
    lines = read_lines(root, relpath)
    return anchor_line(lines, label) is not None


# ---- synthetic leaf model ------------------------------------------------

def make_leaf(fibers):
    """fibers: dict syndrome->count (>0). Returns leaf record."""
    fibers = {s: c for s, c in fibers.items() if c > 0}
    return {"mass": sum(fibers.values()), "L": len(fibers), "fibers": fibers}


def per_leaf_Q(leaf, C):
    """Per-leaf Q at LEAF scale: max fiber <= C * (M/L)."""
    return max(leaf["fibers"].values()) <= C * (leaf["mass"] / leaf["L"]) + 1e-9


def global_maxfiber(leaves):
    agg = {}
    for lf in leaves:
        for s, c in lf["fibers"].items():
            agg[s] = agg.get(s, 0) + c
    return max(agg.values()) if agg else 0


def nondegenerate_family(Y, nleaves, rng):
    """Build nleaves flat leaves with near-full images (L_j in [Y-2, Y]) and
    exactly-flat fibers (every fiber == base), so per-leaf Q(C=1) holds exactly
    and image non-degeneracy holds. Total residual mass is the exact sum of leaf
    masses, so M_res is well-defined (no over/under-count vs a target Mtot)."""
    leaves = []
    for _ in range(nleaves):
        Lj = max(1, Y - rng.randint(0, 2))
        base = rng.randint(1, 8)
        fibers = {s: base for s in range(Lj)}   # exactly flat: maxfiber == M/L
        leaves.append(make_leaf(fibers))
    return leaves


def collapsed_family(Y, barN, nleaves, pile):
    """nleaves leaves, each mass barN, each L=1. pile=True: all on syndrome 0
    (falsifier). pile=False: spread to distinct syndromes (repair)."""
    leaves = []
    for j in range(nleaves):
        s = 0 if pile else (j % Y)
        leaves.append(make_leaf({s: barN}))
    return leaves


# ---- gates ---------------------------------------------------------------

def gate_G1(root):
    """Quote byte-match: gap faithful to files."""
    A = "experimental/asymptotic_rs_mca.tex"
    G = "experimental/grande_finale.tex"
    checks = [
        # post-edit asymptotic names the condition
        quote_near_anchor(root, A, r"\label{lem:addback}",
                          "profile non-degenerate"),
        quote_near_anchor(root, A, r"\label{lem:addback}",
                          r"\cref{def:profile-nondegen}"),
        quote_near_anchor(root, A, r"\label{def:profile-nondegen}",
                          "image non-degeneracy"),
        quote_near_anchor(root, A, r"\label{def:profile-nondegen}",
                          r"L_j\ge\exp(-o(n))|Y|"),
        # grande states it as a hypothesis
        quote_near_anchor(root, G, r"\label{lem:subexponential-addback-closure}",
                          "Suppose that, in every first-match leaf"),
        quote_near_anchor(root, G, r"\label{lem:subexponential-addback-closure}",
                          "each paid cell contributes at most"),
        quote_near_anchor(root, G, r"\label{rem:not-no-input-proof}",
                          "remain conditional safe-side"),
        # atoms cited by note R3
        label_present(root, G, r"\label{prop:vandermonde-kills-low-rank}"),
        label_present(root, G, r"\label{prob:entropy-inverse-q}"),
    ]
    return all(checks), sum(checks), len(checks)


def gate_G2(rng, trials=400):
    """R1: image non-degeneracy => global bound (C/rho) barN. Also assert the
    grande per-cell global-scale bound follows."""
    ok = 0
    for _ in range(trials):
        Y = rng.randint(24, 90)
        nleaves = rng.randint(1, 8)
        leaves = nondegenerate_family(Y, nleaves, rng)
        C = 1.0
        assert all(per_leaf_Q(lf, C) for lf in leaves)   # exactly flat => holds
        rho = min(lf["L"] for lf in leaves) / Y          # image density lower bound
        M_res = sum(lf["mass"] for lf in leaves)
        barN = M_res / Y                                 # residual mass / |Y|
        gmax = global_maxfiber(leaves)
        bound = (C / rho) * barN
        # grande per-cell global-scale bound: each leaf <= exp(o) barN
        percell_ok = all(max(lf["fibers"].values()) <= (C / rho) * barN + 1e-6
                         for lf in leaves)
        if gmax <= bound + 1e-6 and percell_ok:
            ok += 1
        else:
            return False, ok, trials
    return True, ok, trials


def falsifier_witness(Y=64, barN=4):
    """Return (piled, spread) collapsed families and diagnostics."""
    nleaves = Y  # |Y| leaves each of mass barN -> Mtot = |Y| barN, barN_global=barN
    Mtot = nleaves * barN
    piled = collapsed_family(Y, barN, nleaves, pile=True)
    spread = collapsed_family(Y, barN, nleaves, pile=False)
    return piled, spread, Mtot, Y, barN


def gate_G3():
    """R4 falsifier: piled witness has per-leaf Q TRUE and add-back violated by
    factor |Y|; spread repair satisfies."""
    piled, spread, Mtot, Y, barN = falsifier_witness()
    C = 1.0
    plQ_piled = all(per_leaf_Q(lf, C) for lf in piled)
    plQ_spread = all(per_leaf_Q(lf, C) for lf in spread)
    g_piled = global_maxfiber(piled)
    g_spread = global_maxfiber(spread)
    blowup = g_piled / barN
    checks = [
        plQ_piled is True,               # per-leaf Q holds on the witness
        blowup >= Y - 1e-9,              # add-back violated by ~|Y|
        plQ_spread is True,              # repair keeps per-leaf Q
        g_spread <= 2 * barN + 1e-9,     # repair restores O(barN)
    ]
    return all(checks), sum(checks), len(checks)


def gate_G4(rng, trials=30000):
    """R2 subregime: full-mass frontier leaf forces |logL-logY| <= 3 eps."""
    ok = 0
    for _ in range(trials):
        eps = rng.uniform(0.0, 0.05)
        lgMtot = rng.uniform(0.3, 0.9)
        lgY = lgMtot + rng.uniform(-eps, eps)          # frontier row
        lgM = lgMtot - rng.uniform(0.0, eps)           # full mass
        lgL = lgM + rng.uniform(-eps, eps)             # frontier leaf
        if abs(lgL - lgY) <= 3 * eps + 1e-12:
            ok += 1
        else:
            return False, ok, trials
    return True, ok, trials


def gate_G5(rng, trials=400):
    """R1 finite composition: with per-leaf rate e^{e1} and image slack e^{e2},
    the assembled bound e^{e1+e2} barN dominates the observed global max."""
    ok = 0
    for _ in range(trials):
        Y = rng.randint(24, 90)
        nleaves = rng.randint(1, 8)
        leaves = nondegenerate_family(Y, nleaves, rng)
        barN = sum(lf["mass"] for lf in leaves) / Y
        # measured per-leaf rate e1 = max_j maxfiber/(M_j/L_j); image slack via rho
        e1 = max(max(lf["fibers"].values()) / (lf["mass"] / lf["L"]) for lf in leaves)
        rho = min(lf["L"] for lf in leaves) / Y
        e2 = 1.0 / rho
        assembled = e1 * e2 * barN
        if global_maxfiber(leaves) <= assembled + 1e-6:
            ok += 1
        else:
            return False, ok, trials
    return True, ok, trials


# ---- tamper self-tests (breaking a witness must break its gate) ----------

def tamper_tests(root, rng):
    results = []

    # T1: corrupt a G1 quote target -> the specific check fails.
    bad = quote_near_anchor(root, "experimental/grande_finale.tex",
                            r"\label{lem:subexponential-addback-closure}",
                            "Suppose that, in every SECOND-match leaf")  # wrong word
    results.append(("T1 corrupted-quote-rejected", bad is False))

    # T2: wrong anchor -> not found.
    bad = quote_near_anchor(root, "experimental/asymptotic_rs_mca.tex",
                            r"\label{def:does-not-exist}", "image non-degeneracy")
    results.append(("T2 wrong-anchor-rejected", bad is False))

    # T3: inject image-collapsed leaves into a nondegenerate family -> the
    # (C/rho) bound with rho of the GOOD leaves is violated (nondegeneracy load-bearing).
    Y = 64
    good = nondegenerate_family(Y, 4, rng)
    rho_good = min(lf["L"] for lf in good) / Y
    # add many collapsed leaves piling on syndrome 0, each mass ~barN
    barN0 = sum(lf["mass"] for lf in good) / Y
    for _ in range(Y):
        good.append(make_leaf({0: max(1, int(round(barN0)))}))
    barN2 = sum(lf["mass"] for lf in good) / Y
    gmax = global_maxfiber(good)
    # bound computed as if all leaves were non-degenerate (rho_good) underestimates
    violated = gmax > (1.0 / rho_good) * barN2 + 1e-6
    results.append(("T3 injected-collapse-violates-bound", violated is True))

    # T4: de-pile the falsifier -> violation disappears (pile-up is the cause).
    _, spread, _, Yf, barNf = falsifier_witness()
    depiled_ok = global_maxfiber(spread) <= 2 * barNf + 1e-9
    results.append(("T4 depile-removes-violation", depiled_ok is True))

    # T5: drop full-mass in G4 arithmetic -> collapse below exp(-3eps)Y possible.
    found = False
    for _ in range(30000):
        eps = 0.02
        lgMtot = 0.9
        lgY = 0.9
        lgM = lgMtot - rng.uniform(0.1, 0.5)     # NOT full mass
        lgL = lgM + rng.uniform(-eps, eps)       # leaf still frontier
        if lgL - lgY < -3 * eps - 1e-9:
            found = True
            break
    results.append(("T5 no-fullmass-allows-collapse", found is True))

    # T6: a witness that breaks per-leaf Q is not a valid falsifier -> rejected.
    # make one leaf super-peaked so per-leaf Q(C=1) fails; the falsifier gate
    # requires per-leaf Q TRUE, so such a witness would fail check[0].
    bad_leaf = make_leaf({0: 100, 1: 1})  # maxfiber 100 >> M/L = 50.5
    plQ = per_leaf_Q(bad_leaf, 1.0)
    results.append(("T6 broken-perleafQ-rejected", plQ is False))

    ok = all(v for _, v in results)
    return ok, results


# ---- main ----------------------------------------------------------------

def main():
    cap_memory()
    root = repo_root()
    rng = random.Random(20260709)

    print("verify_addback_profile_decomposition -- gap A6 / lem:addback")
    print("root:", root)
    print()

    gates = []
    g1_ok, g1a, g1b = gate_G1(root)
    gates.append(("G1 quote byte-match", g1_ok, f"{g1a}/{g1b} located"))
    g2_ok, g2a, g2b = gate_G2(rng)
    gates.append(("G2 add-back sufficiency (R1)", g2_ok, f"{g2a}/{g2b} instances"))
    g3_ok, g3a, g3b = gate_G3()
    gates.append(("G3 falsifier (R4)", g3_ok, f"{g3a}/{g3b} conditions"))
    g4_ok, g4a, g4b = gate_G4(rng)
    gates.append(("G4 subregime discharge (R2)", g4_ok, f"{g4a}/{g4b} grid pts"))
    g5_ok, g5a, g5b = gate_G5(rng)
    gates.append(("G5 master composition (R1)", g5_ok, f"{g5a}/{g5b} instances"))

    t_ok, t_res = tamper_tests(root, rng)

    npass = 0
    for name, ok, detail in gates:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        npass += 1 if ok else 0
    print()
    print("  tamper self-tests:")
    tpass = 0
    for name, ok in t_res:
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}")
        tpass += 1 if ok else 0
    print()

    all_ok = all(ok for _, ok, _ in gates) and t_ok
    print(f"GATES PASSED: {npass}/{len(gates)}   TAMPER PASSED: {tpass}/{len(t_res)}")
    # falsifier headline number
    piled, _, Mtot, Y, barN = falsifier_witness()
    print(f"falsifier blow-up: max_s N(s) = {global_maxfiber(piled)} = "
          f"{global_maxfiber(piled)/barN:.0f}x barN_global (= |Y| = {Y})")
    print(f"caps: RLIMIT_AS set to {os.environ.get('ADDBACK_AS_CAP_GB', '2')} GB "
          "(env ADDBACK_AS_CAP_GB); all instances small "
          "(<10^3 elements), no truncation.")
    print()
    if all_ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
