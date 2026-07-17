# M1 KoalaBear rank-nine GM--MDS fixed-domain gate v1

This folder contains the canonical JSON certificate for the fail-closed
eleven-locator GM--MDS/fixed-domain trichotomy.  The artifact includes three
exact same-shape controls over `GF(127)`:

- a GM--MDS intersection failure with an emitted common core;
- a GM--MDS-admissible fixed-domain specialization exception of rank ten;
- a GM--MDS-admissible full-rank eleven-locator family.

It also includes a transparent three-quadratic specialization exception over
`GF(11)`.  There is no deployed support tuple, no owner payment, and no
ledger movement.

The implementations are `CONTROL_ONLY_J10`.  Their sequential coefficient
builder is not a deployed-scale executor for `j=981104`; a product-tree/NTT
backend or streamed exact nonzero-minor certificate is still required.  A
full-rank control tuple therefore receives only
`FIXED_DOMAIN_LOCATOR_INDEPENDENCE_CERTIFIED_FOR_DECLARED_TUPLE`.  The
deployed terminal additionally requires retained-slope and first-match
provenance.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.py --check
python3 experimental/scripts/verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.sage
```

To regenerate the canonical artifact after an intentional source change:

```bash
python3 experimental/scripts/verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.py --write
```

The Python verifier recomputes source hashes, all `2^11-1=2047`
intersection tests, exact prime-field locator ranks, null relations, scope
guards, and the payload hash.  The Sage script independently reconstructs
the finite-field arithmetic.
