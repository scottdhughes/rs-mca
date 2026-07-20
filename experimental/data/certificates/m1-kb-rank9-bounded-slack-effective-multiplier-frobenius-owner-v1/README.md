# M1 KoalaBear bounded-slack effective-multiplier owner certificate

This directory binds the exact certificate for the pair-global 392-anchor
source-Frobenius owner.  It replaces the earlier four-anchor slot, closes all
full-outside slack layers \(1\le r\le195\), and records \(r=196\) as the
first layer that the inherited rank-nine aggregate-excess ledger cannot pay.

Replay from the repository root:

    python3 experimental/scripts/verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.py --check
    python3 -O experimental/scripts/verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.py --check
    python3 experimental/scripts/verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.py --tamper-selftest
    python3 -O experimental/scripts/verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.py --tamper-selftest
    /usr/local/bin/sage experimental/scripts/verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.sage
    /usr/local/bin/sage -python -O experimental/scripts/verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.sage.py

Regenerate the JSON only after every bound source is frozen:

    python3 experimental/scripts/verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.py --write

The symbolic proof is the companion note.  Sage supplies an exact degree-two
specialization, falsification controls, and deployed integer endpoint checks;
it does not instantiate a deployed selector or prove the KoalaBear row.

The owner slot cap changes from \(2(p+1)\) to \(196(p+1)\), so the exact
increment is \(194(p+1)\).  The local algebra remains valid through
\(m=9{,}208\), but that larger cap is not banked.  The exhaustive optimizer
certifies \(m=195\) as the last value preserving the inherited one-cut and
nonnegative aggregate-excess gate.

The \(r\ge196\) full-outside residual, non-full-outside source load, \(U_Q\),
residual \(U_A\), complete profile envelope, lower reserve, rank nine, and
KoalaBear remain open.
