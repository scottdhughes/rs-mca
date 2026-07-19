# One-slack common-twist source-subline owner v1

This packet certifies the exact first-match splice and arithmetic for the
pair-global (B)-subline owner that closes
`UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST` at the KoalaBear M1 rank-nine
one-slack frontier.

The JSON is fail-closed and source-bound.  The Python verifier checks exact
row arithmetic, predecessor contracts, owner order, deletion/restart rules,
ledger movement, the downstream rank-nine one-cut arithmetic, and semantic
mutations.  The Sage control checks the three-label projective geometry and
the exact two-label Frobenius pole/coset recovery over `GF(13^2)`.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.py --check
python3 -O experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.py --check
python3 experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.py --tamper-selftest
sage experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.sage
sage -python -O experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.sage.py
```

Regenerate the JSON after an intentional source change:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.py --write
```

Scope: the symbolic note proves one local owner and its subset-stable
post-deletion exclusion.  The toy control is not a deployed selector or
proof.  The moving-cofactor one-slack component, non-full-outside source
load, residual `U_A`, `U_Q`, the complete profile envelope, the unsafe-side
reserve, and the KoalaBear row remain open.
