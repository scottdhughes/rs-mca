# One-slack moving-cofactor source-Frobenius owner v1

This packet certifies the exact first-match splice and arithmetic for the
pair-global four-anchor source-Frobenius owner that closes
`UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR` at the KoalaBear M1
rank-nine one-slack frontier.

The JSON is fail-closed and source-bound. The Python verifier checks the
moving-cofactor normal form, source-only eliminant contract, nonvanishing
dichotomy, canonical owner, deletion/restart rules, ledger movement, revised
source floor, and downstream rank-nine one-cut arithmetic. The Sage control
checks the determinant and Segre-ruling interfaces over `GF(13^2)`.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.py --check
python3 -O experimental/scripts/verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.py --check
python3 experimental/scripts/verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.py --tamper-selftest
sage experimental/scripts/verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.sage
sage -python -O experimental/scripts/verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.sage.py
```

Regenerate the JSON after an intentional source change:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.py --write
```

Scope: the symbolic note proves one local owner and its subset-stable
post-deletion exclusion. The toy control is not a deployed selector or proof.
The `r>=2` full-outside residual, non-full-outside source load, residual
`U_A`, `U_Q`, the complete profile envelope, lower reserve, rank nine, and
KoalaBear remain open.
