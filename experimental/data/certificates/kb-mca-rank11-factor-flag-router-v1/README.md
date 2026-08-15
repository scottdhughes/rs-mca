# KoalaBear rank-eleven factor-flag certificate

This directory freezes the exact integer result for the centered two-level
support-flag router.

Replay from the repository root:

```sh
python3 experimental/scripts/verify_kb_mca_rank11_factor_flag_router_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_factor_flag_router_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank11_factor_flag_router_v1.py
```

The certificate proves a structural terminal only.  It moves no active-v4
ledger value and does not claim affine error rank eleven or KoalaBear closed.
