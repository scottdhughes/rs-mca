# KoalaBear rank-eleven parent synchronization certificate

This directory records the exact deployed arithmetic for the successor to the
anchored rich-flat router.

## Replays

```bash
python3 experimental/scripts/verify_kb_mca_rank11_parent_synchronization_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_parent_synchronization_v1.py --json
python3 experimental/scripts/verify_kb_mca_rank11_parent_synchronization_v1.py --tamper-selftest
python3 experimental/scripts/audit_kb_mca_rank11_parent_synchronization_v1.py
```

Expected status lines:

```text
KB_MCA_RANK11_PARENT_SYNC_PASS
KB_MCA_RANK11_PARENT_SYNC_TAMPER_PASS mutations=7/7
KB_MCA_RANK11_PARENT_SYNC_AUDIT_PASS
```

The certificate proves parent abundance, common-zero synchronization, and
weighted coordinate pinning. It does not assert a complete rank-eleven
payment, KoalaBear closure, or active-v4 ledger movement.