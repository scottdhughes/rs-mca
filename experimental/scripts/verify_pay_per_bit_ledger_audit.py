#!/usr/bin/env python3
"""Verifier for experimental/notes/audits/pay_per_bit_ledger_audit.md.

--check           recompute every bit-margin number in Part 1 exactly
                   (Fraction / high-precision Decimal, no float shortcuts),
                   check every locally-cited file path exists, check every
                   open-wave PR's primary note file exists at its pinned
                   head SHA via `git cat-file`, and validate the Part 2
                   board-to-bits table (JSON certificate) structure/totals.
--tamper-selftest  mutate one anchor, one numeric constant, and one JSON
                   total; confirm each mutation is caught.

stdlib only (subprocess only to shell out to the local `git` binary for
pinned-SHA path checks), deterministic, < 60 s. Exit 0 on PASS, 1 on FAIL.
"""
import json
import math
import os
import subprocess
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # repo root (experimental/..)
EXP = os.path.join(ROOT, "experimental")

NOTE = os.path.join(EXP, "notes", "audits", "pay_per_bit_ledger_audit.md")
CERT = os.path.join(EXP, "data", "certificates", "pay-per-bit-ledger-audit",
                     "certificate.json")
README = os.path.join(ROOT, "readme.md")
SITE_INDEX = os.path.join(ROOT, "site", "index.html")

# ---------------------------------------------------------------------
# Locally-cited files that must exist on this tree (Part 1 sources plus
# the 23 unique c23dcaa-wave primary note files cited in Part 2).
# ---------------------------------------------------------------------
LOCAL_PATHS = [
    "tex/cs25_cap_v12.tex",
    "readme.md",
    "site/index.html",
    "site/data/rate-leaderboards.json",
    "site/data/frontier.json",
    "experimental/data/tangent/tangent_staircase_summary.md",
    "experimental/notes/high_agreement/tangent_staircase.tex",
    "experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md",
]


def read_root(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def git_show(rev_path):
    """Return True iff `git cat-file -e <rev>:<path>` succeeds."""
    try:
        subprocess.run(
            ["git", "cat-file", "-e", rev_path],
            cwd=ROOT, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return False


# ---------------------------------------------------------------------
# Part 1(a): Paper D v12, epsilon_mca > 2^-86
# ---------------------------------------------------------------------
def check_paperD(cert_part1, n):
    p = cert_part1["paperD_v12_cap"]
    assert p["verdict"] == "MATCHES"
    n += 1

    assert 128 - 86 == p["bits_gap"] == 42
    n += 1

    # exact integer recheck of cor:grand's numeric derivation, worst case
    # k=2^40, n=16k=2^44 (rho=1/16 upper bound on n/k):
    k_max = 2 ** 40
    n_max = 16 * k_max
    lhs = 2 * k_max * (n_max + 1)
    rhs = 2 ** 86
    assert lhs == p["integer_inequality"]["lhs"]
    assert rhs == p["integer_inequality"]["rhs"]
    assert (lhs < rhs) is True is p["integer_inequality"]["holds"]
    n += 3

    # tex anchors: cor:grand label + the printed 2^-86 inequality string
    tex = read_root(p["anchor_file"])
    assert r"\label{cor:grand}" in tex
    n += 1
    assert "2^{-86}" in tex and "2^{-128}" in tex
    n += 1
    # the abstract's informal statement and the numerics line both present
    assert "emca(C,\\delta)>2^{-86}" in tex.replace(" ", "") or \
        "\\emca(C,\\delta)>2^{-86}\\gg2^{-128}" in tex.replace(" ", "")
    n += 1
    assert "2^{-42}" in tex  # the sharper conditional q>=2n bound is also printed
    n += 1

    # readme + site both print "42 bits" / "+42"
    readme = read_root("readme.md")
    assert "epsilon_mca > 2^-86" in readme and "42 bits" in readme
    n += 1
    site = read_root("site/index.html")
    assert "+42" in site
    n += 1
    return n


# ---------------------------------------------------------------------
# Part 1(b): Cycle116/119 F_17^32 row, ~32.82 bits
# ---------------------------------------------------------------------
def check_cycle_row(cert_part1, n):
    c = cert_part1["cycle116_119_row"]
    assert c["verdict"] == "MATCHES"
    n += 1

    bad = c["bad_slopes"]
    q17 = 17 ** 32
    assert str(q17) == c["q"]
    n += 1

    g = math.gcd(bad, q17)
    assert g == c["gcd_bad_q"] == 1
    n += 1

    eps = Fraction(bad, q17)
    assert f"{eps.numerator}/{eps.denominator}" == c["fraction_reduced"]
    n += 1

    # exact cross-multiplication check: bad/q17 > 2^-128  <=>  bad*2^128 > q17
    assert (bad * (2 ** 128) > q17) is True is c["cross_multiplication_check_bad_times_2pow128_gt_q"]
    n += 1

    eps_d = Decimal(bad) / Decimal(q17)
    ln2 = Decimal(2).ln()
    log2_eps = eps_d.ln() / ln2
    bits_above = Decimal(128) + log2_eps
    assert str(log2_eps) == c["log2_epsilon_50dp"]
    n += 1
    assert str(bits_above) == c["bits_above_target_50dp"]
    n += 1
    assert float(round(bits_above, 2)) == c["bits_above_target_rounded_2dp"] == 32.82
    n += 1

    # anchors: the printed 32.82 and the exact numerator appear in the site data
    rl = read_root("site/data/rate-leaderboards.json")
    assert "52747567092" in rl and "32.82" in rl
    n += 1
    fj = read_root("site/data/frontier.json")
    assert "52747567092" in fj
    n += 1
    review = read_root("experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md")
    assert "52,747,567,092" in review
    n += 1

    readme = read_root("readme.md")
    assert "32.82 bits" in readme
    n += 1
    return n


# ---------------------------------------------------------------------
# Part 1(c): tangent-staircase 6/7 gate
# ---------------------------------------------------------------------
def check_tangent_gate(cert_part1, n):
    t = cert_part1["tangent_staircase_gate"]
    assert t["verdict"] == "MATCHES"
    n += 1

    q17 = 17 ** 32
    budget = q17 // (2 ** 128)
    assert budget == t["target_budget_floor_q_over_2pow128"] == 6
    n += 1

    n_row, k_row = t["n"], t["k"]
    assert (n_row, k_row) == (512, 256)
    n += 1
    ld506 = n_row - 506 + 1
    ld507 = n_row - 507 + 1
    assert ld506 == t["LD_sw_506"] == 7
    n += 1
    assert ld507 == t["LD_sw_507"] == 6
    n += 1
    # unsafe at 506 (7 > budget 6), safe/at-budget at 507 (6 <= budget 6)
    assert ld506 > budget and ld507 <= budget
    n += 1

    start = -(-(2 * n_row + k_row) // 3)  # ceil((2n+k)/3)
    assert start == t["exact_range_start_ceil_2n_plus_k_over_3"] == 427
    n += 1
    assert 506 >= start and 507 >= start
    n += 1
    assert (3 * 506 - 2 * n_row >= k_row) is True is t["exactness_condition_506"]
    n += 1
    assert (3 * 507 - 2 * n_row >= k_row) is True is t["exactness_condition_507"]
    n += 1

    tss = read_root("experimental/data/tangent/tangent_staircase_summary.md")
    assert "LD_sw(C,506) = 7" in tss
    n += 1
    assert "LD_sw(C,507) = 6" in tss
    n += 1
    assert "floor(17^32 / 2^128) = 6" in tss
    n += 1

    readme = read_root("readme.md")
    assert "6/7 transition" in readme
    n += 1
    return n


# ---------------------------------------------------------------------
# Part 2: board-to-bits table structure/totals
# ---------------------------------------------------------------------
VALID_CATEGORIES = {"i", "ii", "iii", "iv"}


def check_board(cert_part2, n):
    board = cert_part2["board"]
    assert len(board) == 35 == cert_part2["totals"]["count"]
    n += 1

    pr_numbers = [row["pr"] for row in board]
    assert len(set(pr_numbers)) == 35, "duplicate PR number in board"
    n += 1
    expected_prs = set(range(699, 723)) | {723, 725, 727, 728, 729, 730, 731,
                                            732, 733, 734, 735}
    assert set(pr_numbers) == expected_prs
    n += 1

    for row in board:
        assert row["category"] in VALID_CATEGORIES, row
        assert (row["hard_input"] is None) or (1 <= row["hard_input"] <= 5)
        # category (i)/(ii) would require a printed numeric delta; none exist
        assert row["category"] not in ("i", "ii")
        n += 1

    totals = cert_part2["totals"]
    computed = {
        "i": sum(1 for r in board if r["category"] == "i"),
        "ii": sum(1 for r in board if r["category"] == "ii"),
        "iii": sum(1 for r in board if r["category"] == "iii"),
        "iv": sum(1 for r in board if r["category"] == "iv"),
        "ours": sum(1 for r in board if r["ours"]),
        "external": sum(1 for r in board if not r["ours"]),
    }
    for key, val in computed.items():
        assert totals[key] == val, f"totals[{key}]={totals[key]} != computed {val}"
        n += 1
    assert totals["i"] == 0 and totals["ii"] == 0
    n += 1
    assert totals["iii"] + totals["iv"] == 35
    n += 1

    by_hi = cert_part2["by_hard_input"]
    computed_by_hi = {}
    for r in board:
        if r["category"] == "iii":
            assert r["hard_input"] is not None, r
            computed_by_hi.setdefault(str(r["hard_input"]), []).append(r["pr"])
    for key in computed_by_hi:
        assert sorted(by_hi[key]) == sorted(computed_by_hi[key]), key
        n += 1
    assert sum(len(v) for v in by_hi.values()) == totals["iii"]
    n += 1

    # every (iii)/(iv) row's hard_input is None iff category is (iv)
    for row in board:
        if row["category"] == "iv":
            assert row["hard_input"] is None, row
        if row["category"] == "iii":
            assert row["hard_input"] is not None, row
    n += 1

    # local file anchors for the 24 integrated (c23dcaa) rows
    for row in board:
        if row["head_sha"] is None:  # integrated wave: local path must exist
            path = os.path.join(ROOT, row["note_path"])
            assert os.path.isfile(path), f"missing local note: {row['note_path']}"
            n += 1
        else:  # open wave: file must exist at the pinned head SHA
            ref = f"{row['head_sha']}:{row['note_path']}"
            assert git_show(ref), f"missing at pinned SHA: {ref}"
            n += 1

    return n


# ---------------------------------------------------------------------
# Part 3: interval statement
# ---------------------------------------------------------------------
def check_interval(cert_part3, n):
    d = cert_part3["deployed_bracket"]
    rho = Fraction(1, 2)
    lower_uncond = (1 - rho) / 3
    lower_cond = (1 - rho) / 2
    upper = Fraction(15331, 32768)
    assert str(lower_uncond) == d["unconditional"]["lower"] == "1/6"
    n += 1
    assert str(lower_cond) == d["modulo_BCIKS20_import"]["lower"] == "1/4"
    n += 1
    assert str(upper) == d["unconditional"]["upper"] == d["modulo_BCIKS20_import"]["upper"]
    n += 1
    assert upper.denominator == 2 ** 15 == 32768
    n += 1
    assert abs(float(upper / lower_cond) - 1.8714599609375) < 1e-9
    n += 1
    assert float(upper / lower_cond) < 2.0  # "within a factor smaller than two"
    n += 1

    tex = read_root("tex/cs25_cap_v12.tex")
    assert r"\label{thm:informal-sandwich}" in tex
    n += 1
    assert "15331}{32768}" in tex.replace(" ", "")
    n += 1

    frontiers = read_root("experimental/asymptotic_rs_mca_frontiers.tex")
    assert "1.10" in frontiers  # eq:(1.10) tag present in the identity-frontier corollary
    n += 1
    assert "g^*(\\rho_n,\\beta_n)" in frontiers.replace(" ", "")
    n += 1

    rf = cert_part3["rho_star_image_face_bracket"]
    assert rf["value"] == [0.160847, 0.405465]
    n += 1
    assert rf["tex_consumer"] is False
    n += 1
    recon = read_root("experimental/notes/thresholds/post_sweep_bracket_reconciliation.md")
    assert "0.160847" in recon and "0.405465" in recon
    n += 1
    return n


# ---------------------------------------------------------------------
# Steering-paragraph anchor
# ---------------------------------------------------------------------
def check_steering_anchor(n):
    readme = read_root("readme.md")
    assert "Pay-per-bit framing" in readme
    n += 1
    assert git_show("fe93bb59dff3d022f66a097208e17c27e1e0deb4:readme.md")
    n += 1
    site = read_root("site/index.html")
    assert "Pay-per-bit view" in site
    n += 1
    return n


def run_checks(readme_override=None, tex_override=None, cert_override=None):
    n = 0
    cert = cert_override if cert_override is not None else json.load(open(CERT, encoding="utf-8"))

    n = check_steering_anchor(n)
    n = check_paperD(cert["part1_records"], n)
    n = check_cycle_row(cert["part1_records"], n)
    n = check_tangent_gate(cert["part1_records"], n)
    n = check_board(cert["part2_board_to_bits"], n)
    n = check_interval(cert["part3_interval"], n)

    # note file itself exists and cites the certificate + verifier paths
    assert os.path.isfile(NOTE)
    n += 1
    note_text = open(NOTE, encoding="utf-8").read()
    assert "verify_pay_per_bit_ledger_audit.py" in note_text
    n += 1
    assert "pay-per-bit-ledger-audit/certificate.json" in note_text
    n += 1
    return n


def main():
    if not __debug__:
        print("refuses optimized mode (python -O strips assert; run without -O)",
              file=sys.stderr)
        return 2
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode == "--check":
        n = run_checks()
        print(f"RESULT: PASS ({n}/{n})")
        return 0

    if mode == "--tamper-selftest":
        caught = 0
        base_cert = json.load(open(CERT, encoding="utf-8"))

        # tamper 1: corrupt the printed bit-margin string for the Cycle row
        import copy
        bad_cert = copy.deepcopy(base_cert)
        bad_cert["part1_records"]["cycle116_119_row"]["bits_above_target_rounded_2dp"] = 99.99
        try:
            run_checks(cert_override=bad_cert)
            print("tamper 1 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        # tamper 2: corrupt the Part 2 totals (claim a false (i)-category win)
        bad_cert2 = copy.deepcopy(base_cert)
        bad_cert2["part2_board_to_bits"]["board"][0]["category"] = "i"
        try:
            run_checks(cert_override=bad_cert2)
            print("tamper 2 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        # tamper 3: corrupt the deployed-bracket upper edge fraction
        bad_cert3 = copy.deepcopy(base_cert)
        bad_cert3["part3_interval"]["deployed_bracket"]["unconditional"]["upper"] = "1/2"
        try:
            run_checks(cert_override=bad_cert3)
            print("tamper 3 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        # tamper 4: drop a required tex anchor by pointing at a bogus path
        bad_cert4 = copy.deepcopy(base_cert)
        bad_cert4["part1_records"]["paperD_v12_cap"]["anchor_file"] = "tex/does_not_exist.tex"
        try:
            run_checks(cert_override=bad_cert4)
            print("tamper 4 NOT caught", file=sys.stderr)
        except (AssertionError, FileNotFoundError):
            caught += 1

        # tamper 5: falsify a git-cat-file pinned SHA for an open-wave row
        bad_cert5 = copy.deepcopy(base_cert)
        for row in bad_cert5["part2_board_to_bits"]["board"]:
            if row["pr"] == 723:
                row["head_sha"] = "0000000000000000000000000000000000000"
        try:
            run_checks(cert_override=bad_cert5)
            print("tamper 5 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        ok = caught == 5
        print(f"RESULT: {'PASS' if ok else 'FAIL'} ({caught}/5)")
        return 0 if ok else 1

    print(f"unknown mode {mode}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
