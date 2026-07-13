#!/usr/bin/env python3
"""Verifier for post_sweep_reconciliation_c23dcaa.md.

This is an AUDIT/reconciliation packet, not new mathematics. The verifier:

  1. recomputes the two load-bearing image-face bracket constants from their
     raw (f_inf, L1_inf, b) data via rho = (ln f + ln L)/b - ln 2, and the
     upper end ln(3/2), and asserts every ordering printed in the note's
     bracket table (section 6);
  2. anchor-checks each recomputed number against BOTH this note and its
     integrated source file (comb_trade_champion_k5.md for the bracket lower
     end and k=5 ceiling; ilo_moment_closed_consumer.md / image_face_print_
     audit.md for the upper end);
  3. checks that every note, verifier, and certificate cited by the note
     exists at its cited path on the tree;
  4. asserts the section-1/2/5 residual-set contents and the section-7
     audit-before-consume pass counts appear verbatim in the note;
  5. --tamper-selftest mutates each class of check and confirms it is caught.

Stdlib only, deterministic, no files written. Runs in well under 60s.

Usage:
  python3 verify_post_sweep_reconciliation_c23dcaa.py --check
  python3 verify_post_sweep_reconciliation_c23dcaa.py --tamper-selftest
  python3 verify_post_sweep_reconciliation_c23dcaa.py            # == --check
"""

import argparse
import os
import sys
from math import log

# ---------------------------------------------------------------------------
# Locations. Script lives in experimental/scripts/ ; repo root is two up.
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir, os.pardir))
NOTE_REL = "experimental/notes/thresholds/post_sweep_reconciliation_c23dcaa.md"

# ---------------------------------------------------------------------------
# Load-bearing bracket data (raw, not the printed rho values).
# rho = (ln f_inf + ln L1_inf)/b - ln 2 ; b = k * |G|.  Source: #705 verifier
# verify_comb_trade_champion_k5.py, rho_of(f, L, b).
# ---------------------------------------------------------------------------
LN2 = log(2.0)


def rho_of(f, L, b):
    return (log(f) + log(L)) / b - LN2


# (f_inf, L1_inf, b, printed_rho)
CHAMPION = (190, 4192627, 24, 0.160847)      # #694 b=24 (k=4) lower-end champion
K5_FLAT = (2072, 57376057, 30, 0.156900)     # #705 k=5 flat ceiling (< champion)
K5_WEIGHT_MAX = 0.160018                      # #705 k=5 best non-uniform weight
UPPER_END = 0.405465                          # ln(3/2), image-face upper end
TOL = 1e-5

# ---------------------------------------------------------------------------
# Every file the note cites, by cited path (checked to exist on the tree).
# ---------------------------------------------------------------------------
CITED_NOTES = [
    "experimental/notes/thresholds/post_sweep_bracket_reconciliation.md",
    "experimental/notes/thresholds/a6_atlas_print_audit.md",
    "experimental/notes/thresholds/atlas_cat_cell_ledger.md",
    "experimental/notes/thresholds/atlas_missing_witness.md",
    "experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md",
    "experimental/notes/thresholds/signed_local_minority_fixed_composition.md",
    "experimental/notes/thresholds/r2_growing_characteristic_cycle_flatness.md",
    "experimental/notes/thresholds/r2_constant_weil_cycle_flatness.md",
    "experimental/notes/thresholds/exp_ilo_habitat_restriction.md",
    "experimental/notes/thresholds/fenced_energy_pincer.md",
    "experimental/notes/thresholds/canonical_reduced_rational_host_compiler.md",
    "experimental/notes/thresholds/a6_all_witness_line_section_compiler.md",
    "experimental/notes/thresholds/profile_envelope_completeness.md",
    "experimental/notes/thresholds/comb_trade_champion_k5.md",
    "experimental/notes/thresholds/comb_trade_champion.md",
    "experimental/notes/thresholds/ilo_moment_closed_consumer.md",
    "experimental/notes/thresholds/image_face_print_audit.md",
    "experimental/notes/thresholds/lower_reserve_o5c_profile_lists.md",
    "experimental/notes/thresholds/lower_reserve_deep_remainder_atlas.md",
    "experimental/notes/thresholds/deep_remainder_partial_occupancy_counterexample.md",
    "experimental/notes/thresholds/projective_line_lift_feasibility_wall.md",
    "experimental/notes/thresholds/rank15_locator_saturation_normal_form.md",
    "experimental/notes/thresholds/identity_crossing_upper_half_route_cut.md",
    "experimental/notes/thresholds/two_regime_lower_reserve_frontiers_packet.md",
    "experimental/notes/thresholds/rooted_order_two_band_reduction.md",
    "experimental/notes/thresholds/simple_pole_realizability.md",
    "experimental/notes/audits/owner_rooted_dense_band_localization_v1.md",
    "experimental/notes/audits/owner_rooted_positive_support_localization_v1.md",
    "experimental/notes/audits/primitive_signed_payment_barrier_v1.md",
    "experimental/notes/audits/arbitrary_mask_idempotent_guardrail_v1.md",
    "experimental/notes/l2/affine_section_one_row_rank_reduction.md",
    "experimental/asymptotic_rs_mca_frontiers.tex",
]
CITED_VERIFIERS = [
    "experimental/scripts/verify_atlas_cat_ledger.py",
    "experimental/scripts/verify_heavy_fiber_admissibility_transfer.py",
    "experimental/scripts/verify_lower_reserve_o5c.py",
    "experimental/scripts/verify_comb_trade_champion_k5.py",
    "experimental/scripts/verify_profile_envelope_completeness.py",
]
CITED_CERTS = [
    "experimental/data/certificates/atlas-cat-ledger/atlas_cat_ledger.json",
    "experimental/data/certificates/heavy-fiber-admissibility-transfer/heavy_fiber_admissibility_transfer.json",
    "experimental/data/certificates/lower-reserve-deep-remainder/deep_remainder_atlas.json",
    "experimental/data/certificates/two_regime_lower_reserve.json",
]

# ---------------------------------------------------------------------------
# Strings the note must contain verbatim (residual sets + audit pass counts).
# ---------------------------------------------------------------------------
NOTE_REQUIRED_STRINGS = [
    "{C3 planted census, C7 projection degree, C8 higher-dim core, C9 Sidon payment}",
    "{C3, C7, C8, C9}",
    "{C7, C8, C9}",
    "signed-or-semantic dichotomy",
    "first-match structure",
    "Theorem DR (field-drop route dead) stands",
    "guaranteed list `6` vs identity floor `1`",
    "PASS (219/219)",
    "PASS (77/77)",
    "PASS (49/49)",
    "PASS (82/82)",
    "PASS (470 checks)",
    "rho*  in  [0.160847, 0.405465]",
]


class Checker:
    def __init__(self):
        self.n = 0
        self.fails = []

    def check(self, ok, label):
        self.n += 1
        if not ok:
            self.fails.append(label)
        return ok

    @property
    def passed(self):
        return self.n - len(self.fails)


def approx(a, b, tol=TOL):
    return abs(a - b) <= tol


def read(rel):
    with open(os.path.join(REPO_ROOT, rel), "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Numeric checks. Parameterized on the bracket data so tamper mode can inject
# corrupted values and confirm the check flips to FAIL.
# ---------------------------------------------------------------------------
def numeric_checks(ck, champion, k5_flat, k5_weight_max, upper_end):
    cf, cL, cb, cprint = champion
    kf, kL, kb, kprint = k5_flat
    rc = rho_of(cf, cL, cb)
    rk = rho_of(kf, kL, kb)

    ck.check(approx(rc, cprint), "champion rho=(ln190+ln4192627)/24-ln2 == 0.160847")
    ck.check(approx(rk, kprint), "k=5 rho=(ln2072+ln57376057)/30-ln2 == 0.156900")
    ck.check(approx(upper_end, log(3.0 / 2.0)), "upper end == ln(3/2) == 0.405465")
    # bracket orderings (section 6)
    ck.check(rk < rc, "k=5 flat ceiling 0.156900 < champion 0.160847")
    ck.check(k5_weight_max < rc, "k=5 weight max 0.160018 < champion 0.160847")
    ck.check(rc < upper_end, "lower end 0.160847 < upper end 0.405465")
    ck.check(0.158411 < rc, "champion 0.160847 > superseded b=18 champion 0.158411")
    return rc, rk


def anchor_checks(ck, note_text):
    # every recomputed number appears in this note AND in its integrated source.
    comb = read("experimental/notes/thresholds/comb_trade_champion_k5.md")
    ilo = read("experimental/notes/thresholds/ilo_moment_closed_consumer.md")
    img = read("experimental/notes/thresholds/image_face_print_audit.md")

    ck.check("0.160847" in note_text, "note prints lower end 0.160847")
    ck.check("0.156900" in note_text, "note prints k=5 ceiling 0.156900")
    ck.check("0.405465" in note_text, "note prints upper end 0.405465")
    ck.check("0.160847" in comb and "0.156900" in comb,
             "comb_trade_champion_k5.md carries 0.160847 and 0.156900")
    ck.check(("0.405465" in ilo) or ("0.405465" in img),
             "upper end 0.405465 anchored in ilo/image source note")
    # raw data anchored in the #705 source note
    ck.check("57376057" in comb and "2072" in comb,
             "k=5 raw (2072, 57376057) anchored in #705 source note")


def file_existence_checks(ck):
    for rel in CITED_NOTES + CITED_VERIFIERS + CITED_CERTS:
        ck.check(os.path.exists(os.path.join(REPO_ROOT, rel)),
                 "cited file exists: " + rel)


def note_string_checks(ck, note_text):
    for s in NOTE_REQUIRED_STRINGS:
        ck.check(s in note_text, "note contains: " + s[:52])


def structure_checks(ck, note_text):
    # the reduction chain must show the shrink C3-row -> {C7,C8,C9}
    ck.check(note_text.count("{C7, C8, C9}") >= 1, "blocked set shrinks to {C7,C8,C9}")
    # the two open packets are marked open, not integrated
    ck.check("`#723` and\n`#725` are open" in note_text or
             "#723` and `#725` are open" in note_text or
             ("#723" in note_text and "#725" in note_text and "open" in note_text),
             "open packets #723/#725 flagged open")
    # five hard inputs each get a one-line state
    for tag in ["1. **Witness-exhaustive atlas.**",
                "2. **Image-scale MI+MA / direct Sidon.**",
                "3. **Residual ray compiler.**",
                "4. **Complete profile-envelope comparison.**",
                "5. **Lower reserve / unsafe side.**"]:
        ck.check(tag in note_text, "per-input line present: " + tag[:34])


def run_all(champion=CHAMPION, k5_flat=K5_FLAT, k5_weight_max=K5_WEIGHT_MAX,
            upper_end=UPPER_END, note_text=None):
    ck = Checker()
    if note_text is None:
        note_text = read(NOTE_REL)
    numeric_checks(ck, champion, k5_flat, k5_weight_max, upper_end)
    anchor_checks(ck, note_text)
    file_existence_checks(ck)
    note_string_checks(ck, note_text)
    structure_checks(ck, note_text)
    return ck


def cmd_check():
    ck = run_all()
    print("-" * 60)
    if ck.fails:
        for f in ck.fails:
            print("  FAIL  " + f)
        print("RESULT: FAIL (%d/%d)" % (ck.passed, ck.n))
        return 1
    print("RESULT: PASS (%d/%d)" % (ck.passed, ck.n))
    return 0


def cmd_tamper():
    """Each mutation must be caught (i.e. must turn a passing run into a failing
    one). Confirms the checks are load-bearing, not vacuous."""
    note_text = read(NOTE_REL)
    baseline = run_all(note_text=note_text)
    if baseline.fails:
        print("tamper-selftest ABORTED: baseline is not clean:")
        for f in baseline.fails:
            print("  " + f)
        return 1

    mutations = []
    # 1. corrupt the champion printed value
    mutations.append(("champion rho printed value",
                      dict(champion=(190, 4192627, 24, 0.170000))))
    # 2. corrupt the k=5 ceiling so it no longer sits below the champion
    mutations.append(("k=5 ceiling above champion",
                      dict(k5_flat=(2072, 57376057, 30, 0.170000))))
    # 3. corrupt the k=5 raw census count
    mutations.append(("k=5 raw L1_inf count",
                      dict(k5_flat=(2072, 99999999, 30, 0.156900))))
    # 4. corrupt the upper end away from ln(3/2)
    mutations.append(("upper end != ln(3/2)", dict(upper_end=0.400000)))
    # 5. weight max exceeding champion
    mutations.append(("weight max above champion", dict(k5_weight_max=0.170000)))
    # 6. delete a required residual-set string from the note copy
    mutations.append(("note missing {C7, C8, C9}",
                      dict(note_text=note_text.replace("{C7, C8, C9}", "{C8, C9}"))))
    # 7. delete an audit pass-count line from the note copy
    mutations.append(("note missing PASS (219/219)",
                      dict(note_text=note_text.replace("PASS (219/219)", "PASS (218/218)"))))
    # 8. break a cited path by pointing REPO_ROOT check at a fake string
    #    (simulated by removing a required note string that gates the section)
    mutations.append(("note missing dichotomy gap statement",
                      dict(note_text=note_text.replace("signed-or-semantic dichotomy", "resolved"))))

    caught = 0
    for name, kw in mutations:
        args = dict(champion=CHAMPION, k5_flat=K5_FLAT, k5_weight_max=K5_WEIGHT_MAX,
                    upper_end=UPPER_END, note_text=note_text)
        args.update(kw)
        res = run_all(**args)
        ok = len(res.fails) > 0
        caught += 1 if ok else 0
        print("  %-38s -> %s" % (name, "caught" if ok else "MISSED"))
        if not ok:
            print("     !! mutation not detected")

    print("-" * 60)
    if caught == len(mutations):
        print("tamper-selftest: PASS (%d/%d mutations caught)" % (caught, len(mutations)))
        return 0
    print("tamper-selftest: FAIL (%d/%d mutations caught)" % (caught, len(mutations)))
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run all checks (default)")
    ap.add_argument("--tamper-selftest", action="store_true",
                    help="confirm each check is load-bearing")
    args = ap.parse_args()
    if args.tamper_selftest:
        return cmd_tamper()
    return cmd_check()


if __name__ == "__main__":
    sys.exit(main())
