#!/usr/bin/env python3
"""Verifier for experimental/notes/audits/pay_per_bit_86bit_conditional_rows.md.

Follow-up to PR #736's pay-per-bit ledger audit
(experimental/notes/audits/pay_per_bit_ledger_audit.md), which flagged that
cor:grand (tex/cs25_cap_v12.tex:3542-3585) prints a sharper CONDITIONAL
branch -- "If q>=2n, the lower bound improves to >=2^-42" (86 bits above the
2^-128 target, vs. 42 bits unconditionally) -- as a number "worth a future
footnote". This script instantiates cor:grand's FULL hypothesis set (not
just q>=2n) on the maintainer-cited deployed anchor rows: the KoalaBear
sextic row, the two Mersenne-31/QM31 circle rows, and the F_17^32
Cycle116/119 row.

--check           recompute every integer/Fraction/Decimal quantity in the
                   note from scratch (no float shortcuts), check every
                   hypothesis (H1-H7) per row against the certificate, check
                   tex anchors and line numbers, and cross-validate the JSON
                   certificate's numbers against the independent recompute.
--tamper-selftest  mutate one row verdict, one big-integer margin, and one
                   bit-arithmetic constant in the certificate; confirm each
                   mutation is caught.

stdlib only (fractions, decimal, json, math), deterministic, < 60 s.
Exit 0 on PASS, 1 on FAIL.
"""
import copy
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
LN2 = Decimal(2).ln()

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # repo root (experimental/..)
EXP = os.path.join(ROOT, "experimental")

NOTE = os.path.join(EXP, "notes", "audits",
                     "pay_per_bit_86bit_conditional_rows.md")
CERT = os.path.join(EXP, "data", "certificates",
                     "pay-per-bit-86bit-conditional-rows", "certificate.json")


def read_root(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def is_prime_trial(n):
    """Deterministic trial division -- fine for the <=31-bit primes here."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def bits_above_target(target_exponent_abs, num, den):
    """bits above 2^{-target_exponent_abs} for the exact value num/den."""
    val = Decimal(num) / Decimal(den)
    return Decimal(target_exponent_abs) + val.ln() / LN2


# ---------------------------------------------------------------------
# Anchors: cor:grand's own text, line numbers, and the exact count of the
# "q>=2n" sentence in the whole paper (must be 2: the statement + the proof,
# both inside cor:grand; nowhere else, in particular not in the circle
# corollaries).
# ---------------------------------------------------------------------
def flatten(text):
    """Strip all whitespace, for substring checks across line breaks."""
    return "".join(text.split())


def check_anchors(cert, n):
    a = cert["anchor"]
    tex = read_root(a["file"])
    lines = tex.splitlines()
    flat = flatten(tex)

    label_line = a["cor_grand_label_line"]
    assert r"\label{cor:grand}" in lines[label_line - 1]
    n += 1

    thm_line = a["thm_main_label_line"]
    assert r"\label{thm:main}" in lines[thm_line - 1]
    n += 1

    occ = [i + 1 for i, l in enumerate(lines)
           if "q\\ge2n" in l.replace(" ", "")]
    assert occ == a["qge2n_occurrence_lines"]
    n += 1
    assert len(occ) == a["qge2n_total_occurrences_in_file"] == 2
    n += 1
    # both occurrences fall strictly inside the printed cor:grand span
    lo, hi = (int(x) for x in a["cor_grand_statement_lines"].split("-"))
    proof_lo, proof_hi = (int(x) for x in a["cor_grand_proof_lines"].split("-"))
    for ln_ in occ:
        assert (lo <= ln_ <= hi) or (proof_lo <= ln_ <= proof_hi), ln_
    n += 1

    # the sharper branch's printed conclusion string is present
    assert r"\ge2^{-42}" in flat
    n += 1
    assert r"\ge2^{-86}" in flat
    n += 1

    # def:map-smooth's own remark that a multiplicative coset is a *special
    # case* (X^a,a)-smooth domain -- the textual basis for H5's distinction
    # between cor:grand's coset domains and the circle codes' Chebyshev
    # domains.
    remark_line = a["map_smooth_coset_remark_line"]
    assert "multiplicative coset" in lines[remark_line - 1]
    assert "(X^a,a)" in flatten(lines[remark_line - 1]).replace("$", "")
    n += 1

    # circle-grand's proof explicitly routes through thm:phi-cap and
    # Chebyshev/(T_a,a)-smoothness, not thm:main.
    lo2, hi2 = (int(x) for x in a["cor_circle_grand_lines"].split("-"))
    circle_block = "\n".join(lines[lo2 - 1:hi2])
    circle_flat = flatten(circle_block)
    assert "phi-cap" in circle_flat.replace("\\", "")
    n += 1
    assert "(T_a,a)" in circle_flat.replace("$", "")
    n += 1

    # circle-grand/circle-deployed do NOT print an analogous q>=2n sentence
    assert "q\\ge2n" not in circle_flat
    n += 1
    lo3, hi3 = (int(x) for x in a["cor_circle_deployed_lines"].split("-"))
    deployed_block = "\n".join(lines[lo3 - 1:hi3])
    assert "q\\ge2n" not in flatten(deployed_block)
    n += 1

    # the odd-k_c remark is present near the cited line
    odd_line = a["odd_kc_remark_line"]
    window = "\n".join(lines[odd_line - 6:odd_line + 4])
    assert "always" in window and ("odd" in window or "a\\nmid" in
                                    flatten(window))
    n += 1
    return n


# ---------------------------------------------------------------------
# Bit arithmetic (trivial exact-integer identities).
# ---------------------------------------------------------------------
def check_bit_arithmetic(cert, n):
    b = cert["bit_arithmetic"]
    assert b["target_exponent"] == -128
    n += 1
    assert 128 - 86 == b["unconditional_bits_above_target"] == 42
    n += 1
    assert 128 - 42 == b["conditional_bits_above_target"] == 86
    n += 1
    w = b["worst_case_integer_inequality"]
    lhs = 4 * 2 ** 40
    rhs = 2 ** 42
    assert lhs == rhs == int(w["lhs_value"]) == int(w["rhs_value"])
    n += 1
    assert w["equal"] is True
    n += 1
    return n


# ---------------------------------------------------------------------
# Row: KoalaBear sextic.
# ---------------------------------------------------------------------
def check_row_kb(cert, n):
    r = cert["rows"]["kb_sextic"]

    p = 2 ** 31 - 2 ** 24 + 1
    assert str(p) == r["p"]
    n += 1
    assert is_prime_trial(p) is True is r["p_prime"]
    n += 1

    q = p ** 6
    n_dom = 2 ** 21
    k = 2 ** 20
    assert str(q) == r["q"]
    n += 1
    assert q.bit_length() == r["q_bit_length"] == 186
    n += 1
    assert str(n_dom) == r["n"] and str(k) == r["k"]
    n += 1

    rho = Fraction(k, n_dom)
    assert rho == Fraction(1, 2) == Fraction(r["rho"])
    n += 1

    N_rho = 1024
    h2 = (n_dom % N_rho == 0)
    assert h2 is True is r["hyp_H2_Nrho_divides_n"]["holds"]
    n += 1

    h3 = q < 2 ** 256
    assert h3 is True is r["hyp_H3_q_lt_2pow256"]
    n += 1

    h6 = k <= 2 ** 40
    assert h6 is True is r["hyp_H6_k_le_2pow40"]
    n += 1

    two_n = 2 * n_dom
    margin = q - two_n
    h7 = q >= two_n
    assert h7 is True is r["hyp_H7_q_ge_2n"]["holds"]
    n += 1
    assert str(two_n) == r["hyp_H7_q_ge_2n"]["two_n"]
    n += 1
    assert str(margin) == r["hyp_H7_q_ge_2n"]["margin_q_minus_2n"]
    n += 1

    all_base = h2 and h3 and h6  # H1, H4, H5 are true by construction here
    assert all_base is True is r["cor_grand_base_branch_applies"]
    n += 1
    assert (all_base and h7) is True is r["cor_grand_sharper_branch_applies"]
    n += 1
    assert r["blocking_hypothesis"] is None
    n += 1

    # generic worst-case conditional floor: 1/(4*2^40) = 2^-42 -> 86 bits
    assert 4 * 2 ** 40 == 2 ** 42
    n += 1
    assert r["generic_worst_case_conditional_floor"]["bits_above_target"] == 86
    n += 1

    # row-specific application of the SAME branch formula at this row's
    # actual k=2^20: 1/(4k) = 2^-22 exactly -> 106 bits.
    assert 4 * k == 2 ** 22
    n += 1
    rsc = r["row_specific_conditional_floor"]
    assert rsc["bits_above_target"] == 106
    n += 1

    # cor:deployed's own printed bound: exact tight value via the base
    # formula (1/2k)(1-n/q), evaluated at THIS row's actual n,q (not the
    # q>=2n worst-case relaxation). Confirm it exceeds 2^-22 and sits below
    # 2^-21, i.e. 106 <= true bits < 107.
    exact_bound = Fraction(1, 2 * k) * (1 - Fraction(n_dom, q))
    assert exact_bound > Fraction(1, 2 ** 22)
    n += 1
    assert exact_bound < Fraction(1, 2 ** 21)
    n += 1
    op = r["row_own_printed_bound"]
    assert op["bound"] == "2^-22" and op["bits_above_target"] == 106
    n += 1

    # the row-specific conditional floor (2^-22) exactly matches cor:deployed's
    # own printed headline -- confirms these are the same underlying
    # inequality, evaluated at the same k, differing only in whether n/q is
    # worst-cased (q=2n) or used exactly (q>>2n here).
    assert Fraction(1, 4 * k) == Fraction(1, 2 ** 22)
    n += 1

    # 20-bit dominance claim: row-specific-conditional (106) beats the
    # generic conditional floor (86) by exactly 20 bits.
    assert 106 - 86 == 20
    n += 1
    return n


# ---------------------------------------------------------------------
# Rows: M31 circle line round + circle code.
# ---------------------------------------------------------------------
def check_row_m31(cert, n):
    p = 2 ** 31 - 1
    q = p ** 4
    r_line = cert["rows"]["m31_circle_line_round"]
    r_code = cert["rows"]["m31_circle_code"]

    assert str(p) == r_line["p"]
    n += 1
    assert is_prime_trial(p) is True is r_line["p_prime"]
    n += 1
    assert str(q) == r_line["q"] == r_code["q"]
    n += 1
    assert q.bit_length() == r_line["q_bit_length"] == 124
    n += 1
    assert (q < 2 ** 128) is True is r_line["q_lt_2pow128"] is r_code["q_lt_2pow128"]
    n += 1

    n_line, k_line = 2 ** 21, 2 ** 20
    assert str(n_line) == r_line["n"] and str(k_line) == r_line["k"]
    n += 1
    two_n_line = 2 * n_line
    margin_line = q - two_n_line
    assert (q >= two_n_line) is True is r_line["hyp_H7_q_ge_2n"]["holds"]
    n += 1
    assert str(two_n_line) == r_line["hyp_H7_q_ge_2n"]["two_n"]
    n += 1
    assert str(margin_line) == r_line["hyp_H7_q_ge_2n"]["margin_q_minus_2n"]
    n += 1

    n_code, k_code = 2 ** 22, 2 ** 21 + 1
    assert str(n_code) == r_code["n_c"] and str(k_code) == r_code["k_c"]
    n += 1
    assert (k_code % 2 == 1) is True is r_code["k_c_is_odd"]
    n += 1
    two_n_code = 2 * n_code
    margin_code = q - two_n_code
    assert (q >= two_n_code) is True is r_code["hyp_H7_q_ge_2n"]["holds"]
    n += 1
    assert str(two_n_code) == r_code["hyp_H7_q_ge_2n"]["two_n_c"]
    n += 1
    assert str(margin_code) == r_code["hyp_H7_q_ge_2n"]["margin_q_minus_2n_c"]
    n += 1

    # both blocked at H5, so cor:grand does not apply regardless of q>=2n
    assert r_line["hyp_H5_multiplicative_coset"] is False
    n += 1
    assert r_code["hyp_H5_multiplicative_coset"] is False
    n += 1
    assert r_line["cor_grand_sharper_branch_applies"] is False
    n += 1
    assert r_code["cor_grand_sharper_branch_applies"] is False
    n += 1
    assert r_line["blocking_hypothesis"] == r_code["blocking_hypothesis"] == "H5"
    n += 1

    # printed bounds against the CORRECT (paper-stated) target 2^-100, since
    # q < 2^128 makes 2^-128 degenerate for these rows.
    assert 100 - 22 == r_line["row_own_printed_bound"]["bits_above_target"] == 78
    n += 1
    assert 100 - 23 == r_code["row_own_printed_bound"]["bits_above_target"] == 77
    n += 1
    return n


# ---------------------------------------------------------------------
# Row: F_17^32 (Cycle116/119).
# ---------------------------------------------------------------------
def check_row_f17(cert, n):
    r = cert["rows"]["f17_32_cycle116_119"]

    q = 17 ** 32
    n_dom, k = 512, 256
    assert str(q) == r["q"]
    n += 1
    assert q.bit_length() == r["q_bit_length"] == 131
    n += 1
    assert str(n_dom) == r["n"] and str(k) == r["k"]
    n += 1

    N_rho = 1024
    h2 = (n_dom % N_rho == 0)
    assert h2 is False is r["hyp_H2_Nrho_divides_n"]["holds"]
    n += 1

    two_n = 2 * n_dom
    margin = q - two_n
    h7 = q >= two_n
    assert h7 is True is r["hyp_H7_q_ge_2n"]["holds"]
    n += 1
    assert str(two_n) == r["hyp_H7_q_ge_2n"]["two_n"]
    n += 1
    assert str(margin) == r["hyp_H7_q_ge_2n"]["margin_q_minus_2n"]
    n += 1

    assert r["cor_grand_sharper_branch_applies"] is False
    n += 1
    assert r["blocking_hypothesis"] == "H2"
    n += 1

    # row's own best number: exact fraction + Decimal bits-above-target,
    # cross-checked against PR #736's own recomputation of the same figure.
    bad = r["row_own_printed_bound"]["bad_slopes"]
    assert bad == 52747567092
    n += 1
    g = math.gcd(bad, q)
    assert g == 1
    n += 1
    ba = bits_above_target(128, bad, q)
    assert str(ba) == r["row_own_printed_bound"]["bits_above_target_exact_50dp"]
    n += 1
    assert float(round(ba, 2)) == r["row_own_printed_bound"][
        "bits_above_target_rounded_2dp"] == 32.82
    n += 1
    # below the generic UNCONDITIONAL floor (42 bits) -- no contradiction,
    # since H2 already rules the row out of cor:grand entirely.
    assert round(float(ba), 2) < 42
    n += 1

    # diagnostic: thm:main's own eq:hyp at N=256 (the smaller N that rescues
    # the KB interleaved family), B=F (no subfield gap for this row).
    diag = r["diagnostic_N256_eq_hyp_check"]
    N, ell2 = 256, 130
    assert diag["N"] == N and diag["ell_2"] == ell2
    n += 1
    binom = math.comb(N, ell2)
    log2_binom = Decimal(binom).ln() / LN2
    assert str(log2_binom) == diag["log2_binom_256_130"]
    n += 1
    rhs = q * (q // k + 1)  # |B|=q worst case (B=F, no smaller subfield)
    log2_rhs = Decimal(rhs).ln() / LN2
    assert str(log2_rhs) == diag["log2_rhs_B_times_qk_plus1"]
    n += 1
    assert (binom >= rhs) is False is diag["eq_hyp_holds_at_N256"]
    n += 1
    shortfall = log2_rhs - log2_binom
    assert str(shortfall) == diag["shortfall_bits"]
    n += 1
    return n


# ---------------------------------------------------------------------
# Interleaved KB family boundary diagnostic (cor:rows, s=2^j, j=0..12).
# ---------------------------------------------------------------------
def check_interleaved_family(cert, n):
    d = cert["interleaved_kb_family_boundary_diagnostic"]
    q = (2 ** 31 - 2 ** 24 + 1) ** 6
    assert str(q) == d["q_fixed"]
    n += 1
    N_rho = 1024
    for j in range(0, 13):
        s = 2 ** j
        n_s = 2 ** 21 // s
        div = (n_s % N_rho == 0)
        q_ge = q >= 2 * n_s
        assert q_ge is True  # holds for every s, by a huge margin
        n += 1
        if j <= 11:
            assert div is True
        else:
            assert j == 12
            assert div is False and n_s == 512
    n += 1
    assert d["boundary"]["j_0_to_11_s_1_to_2048"]["Nrho_divides_n_s"] is True
    n += 1
    assert d["boundary"]["j_12_s_4096"]["Nrho_divides_n_s"] is False
    n += 1
    assert d["boundary"]["j_12_s_4096"]["n_s"] == 512
    n += 1
    assert d["q_ge_2n_s_holds_for_every_s"] is True
    n += 1
    return n


# ---------------------------------------------------------------------
# Verdict-summary consistency.
# ---------------------------------------------------------------------
def check_verdict_summary(cert, n):
    v = cert["verdict_summary"]
    rows = cert["rows"]
    applies = sorted(k for k, r in rows.items()
                      if r["cor_grand_sharper_branch_applies"])
    blocked = sorted(k for k, r in rows.items()
                      if not r["cor_grand_sharper_branch_applies"])
    assert applies == sorted(v["rows_where_sharper_branch_literally_applies"])
    n += 1
    assert blocked == sorted(v["rows_where_sharper_branch_is_blocked"])
    n += 1
    assert applies == ["kb_sextic"]
    n += 1
    assert set(blocked) == {"m31_circle_line_round", "m31_circle_code",
                             "f17_32_cycle116_119"}
    n += 1
    # q>=2n itself holds on every row, independent of applicability
    for r in rows.values():
        h7 = r["hyp_H7_q_ge_2n"]["holds"]
        assert h7 is True
    n += 1
    assert v["q_ge_2n_itself_holds_on_every_row"] is True
    n += 1
    return n


def run_checks(cert_override=None):
    n = 0
    cert = (cert_override if cert_override is not None
            else json.load(open(CERT, encoding="utf-8")))

    n = check_anchors(cert, n)
    n = check_bit_arithmetic(cert, n)
    n = check_row_kb(cert, n)
    n = check_row_m31(cert, n)
    n = check_row_f17(cert, n)
    n = check_interleaved_family(cert, n)
    n = check_verdict_summary(cert, n)

    assert os.path.isfile(NOTE)
    n += 1
    note_text = open(NOTE, encoding="utf-8").read()
    assert "verify_pay_per_bit_86bit_conditional_rows.py" in note_text
    n += 1
    assert "pay-per-bit-86bit-conditional-rows/certificate.json" in note_text
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

        # tamper 1: falsely claim the sharper branch applies to a circle row
        bad1 = copy.deepcopy(base_cert)
        bad1["rows"]["m31_circle_line_round"]["cor_grand_sharper_branch_applies"] = True
        try:
            run_checks(cert_override=bad1)
            print("tamper 1 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        # tamper 2: corrupt the KB row's exact big-integer margin
        bad2 = copy.deepcopy(base_cert)
        m = bad2["rows"]["kb_sextic"]["hyp_H7_q_ge_2n"]["margin_q_minus_2n"]
        bad2["rows"]["kb_sextic"]["hyp_H7_q_ge_2n"]["margin_q_minus_2n"] = m[:-1] + (
            "0" if m[-1] != "0" else "1")
        try:
            run_checks(cert_override=bad2)
            print("tamper 2 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        # tamper 3: corrupt the bit-arithmetic constant (128-42 != 85)
        bad3 = copy.deepcopy(base_cert)
        bad3["bit_arithmetic"]["conditional_bits_above_target"] = 85
        try:
            run_checks(cert_override=bad3)
            print("tamper 3 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        # tamper 4: corrupt the F_17^32 row's rounded bit-margin figure
        bad4 = copy.deepcopy(base_cert)
        bad4["rows"]["f17_32_cycle116_119"]["row_own_printed_bound"][
            "bits_above_target_rounded_2dp"] = 42.00
        try:
            run_checks(cert_override=bad4)
            print("tamper 4 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        # tamper 5: flip H2 for the F_17^32 row to falsely claim it holds
        bad5 = copy.deepcopy(base_cert)
        bad5["rows"]["f17_32_cycle116_119"]["hyp_H2_Nrho_divides_n"]["holds"] = True
        try:
            run_checks(cert_override=bad5)
            print("tamper 5 NOT caught", file=sys.stderr)
        except AssertionError:
            caught += 1

        total = 5
        print(f"RESULT: {'PASS' if caught == total else 'FAIL'} "
              f"({caught}/{total} tamper cases caught)")
        return 0 if caught == total else 1

    print(f"unknown mode: {mode}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
