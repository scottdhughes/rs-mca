# M31 coupled escape--Forney--Plucker route-cut certificate

This directory freezes the deterministic output for the local structural
packet in
experimental/notes/thresholds/m31_coupled_escape_forney_plucker_route_cut.md.

The certificate checks:

- the deployed \(16/15\) and \(30/29\) joint-index thresholds;
- the exact \(67/68\) forbidden-hyperplane threshold;
- exhaustive enumeration of the source-valid \(F_{11}\) full exact
  weight-three layer;
- its locator Forney profile and constant joint kernel;
- pairwise collision quotients, normalized escapes, and Plücker
  contractions; and
- the global pair-factor scalar on a second full layer with a genuine common
  core; and
- a fail-closed unpaid terminal with zero ledger movement.

expected.txt is hash-gated by the Python verifier.  sage_expected.txt freezes
the output of the independent Sage-native replay.  The computations support,
but do not replace, the symbolic proofs in the note.

Replay:

    python3 experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py --check --expected experimental/data/certificates/m31-coupled-escape-forney-plucker-route-cut/expected.txt
    python3 experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py --tamper-selftest
    /usr/local/bin/sage experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.sage

The terminal is:

    UNPAID_UNCLASSIFIED_16_COLUMN_COUPLED_PADE_FRAME

No M31 endpoint, owner, add-back, scalar descent, quartic-field transfer, or
ledger payment is claimed.  A fresh hostile audit returned GREEN for the
narrow local theorem and packet route cut, and did not authorize row closure.
