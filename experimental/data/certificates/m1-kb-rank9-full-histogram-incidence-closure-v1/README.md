# M1 KoalaBear full-histogram incidence closure certificate

This directory binds the exact zero-ledger successor to the full-outside
carrier-incidence splice.  The successor applies the all-slope MDS basis
floor and the subset-uniform affine graph-line atlas to the complete selected
set; the source slack simplex is used only to cap contributing rich lines.

Replay from the repository root:

    python3 experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.py --check
    python3 -O experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.py --check
    python3 experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.py --tamper-selftest
    python3 -O experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.py --tamper-selftest
    /usr/local/bin/sage experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.sage

Replay the load-bearing predecessor independently:

    python3 experimental/scripts/verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.py --check
    python3 -O experimental/scripts/verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.py --check
    python3 experimental/scripts/verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.py --tamper-selftest
    python3 -O experimental/scripts/verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.py --tamper-selftest

To regenerate the canonical JSON after all bound sources are frozen:

    python3 experimental/scripts/verify_m1_kb_rank9_full_histogram_incidence_closure_v1.py --write-certificate

The exact full scan proves the two paid ranges `196..67470` and
`209553..913631`.  It leaves precisely `67471..209552`, or 142,082 layers.
For every integer in that residual, the verifier constructs an exact abstract
all-zero-deficit packing of `B_remaining + 1` slopes.  This is a scalar route
cut, not a Reed--Solomon selector or a deployed counterexample.

No ledger value moves.  Deployed determinant/source packing, non-full-outside
source load, `U_Q`, residual `U_A`, rank nine, and KoalaBear remain open.
