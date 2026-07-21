# M31 exact-syzygy coloop elimination and locator-only route cut

This directory pins the exact arithmetic and scope contract for
`experimental/notes/thresholds/m31_direct_padded_forney_frame_route_cut.md`.

PR #1021 supplies the padded `62,295` rank-three bound.  This packet records
three exact facts on the marked M31 source keys:

1. after dividing the common canonical locator, the primitive equal-degree
   padded row has total Forney index sum at most `981,129`;
2. the nonzero common received-word syndrome forces one index at least
   `67,448`, so the first three padded indices sum to at most
   `62,295 < 67,447`; and
3. deleting the distinguished coordinate cannot lower syzygy rank, eliminating
   the earlier abstract rank-two-coloop terminal.

The first two items are an alternate proof/cross-check of #1021, not a novelty
claim.  The new conclusions are exact-syzygy coloop elimination and the
empty-core support route cut.

#1021 supplies the canonical padded frame without an unproved padding bridge.
An exact M31-scale support-only counterfamily
then shows that canonical-size boundary masks, pairwise MDS overlap, low padded Forney--Pluecker rows, no
coloop, and even an empty complementary gcd do not pay the signed occupancy
threshold.  The active terminal is therefore

```text
UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND.
```

The executable certificate pins the deployed integer optimizer, all `259,881`
signed source keys, the exact root-union failure, dependency heads, source
hashes, a 32-color subset-sum count, 45 explicit balanced anchors, all 14,190
anchor-triple deletions, and fail-closed nonclaims.  The Sage replay uses the existing
source-realized `F_31` fixture to recover a complete Forney profile from
Macaulay kernels, constructs three low exact syzygies, verifies every
one-column deletion and all Pluecker complementary-gcd divisibilities, and
replays the two canonical orders of PR #1014's `F_11` counterpacket.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --check
python3 -O experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --check
python3 experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.sage
```

The packet fails closed:

```text
M31 list row: OPEN
ledger movement: 0
owner charge: null
U_Q: null
U_A: null
```
