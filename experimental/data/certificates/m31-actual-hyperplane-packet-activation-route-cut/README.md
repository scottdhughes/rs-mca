# M31 actual-hyperplane packet activation route cut

This directory pins the exact JSON contract for
`experimental/notes/thresholds/m31_actual_hyperplane_packet_activation_route_cut.md`.

The certificate proves three scoped statements:

1. the inherited M31 identity-prefix centre has at least `1,993,678` exact
   boundary supports and therefore contains a parity-free 230-support
   subpacket;
2. an independent complete-Chebyshev-fibre construction realizes the pinned
   parity-free 36-support packet in one literal syndrome hyperplane; and
3. every hypothetical forbidden list activates a rank-36 primitive locator
   row with at least 21 Forney indices below `67,447`, including two rows of
   combined degree at most `53,745`.

It fails closed on global closure and records zero ledger movement.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --check
python3 -O experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --check
python3 experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.sage
```

`manifest.json` is generated canonically by the Python verifier and includes
source hashes.  The Sage script is an independent finite-field replay; its
small literal model is a control, not a deployed-scale enumeration.
